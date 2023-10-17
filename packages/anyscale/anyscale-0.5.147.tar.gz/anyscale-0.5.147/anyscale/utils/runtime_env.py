# pylint:disable=private-import
import copy
import hashlib
import logging
import os
from pathlib import Path
import tempfile
from typing import Any, Callable, Dict, Optional, TYPE_CHECKING
from urllib.parse import urlparse

import click

from anyscale.cli_logger import BlockLogger
from anyscale.client.openapi_client import ComputeTemplate
from anyscale.client.openapi_client.api.default_api import DefaultApi
from anyscale.client.openapi_client.models.cloud_providers import CloudProviders
from anyscale.client.openapi_client.models.cloud_with_cloud_resource import (
    CloudWithCloudResource,
)
from anyscale.client.openapi_client.models.cloud_with_cloud_resource_gcp import (
    CloudWithCloudResourceGCP,
)
from anyscale.client.openapi_client.models.user_info import UserInfo
from anyscale.shared_anyscale_utils.aws import bucket_name_from_maybe_bucket_arn
from anyscale.util import is_anyscale_workspace
from anyscale.utils.ray_utils import zip_directory  # type: ignore
from anyscale.utils.workload_types import Workload


if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)


def _upload_file_to_google_cloud_storage(file: str, bucket: str, object_name: str):
    try:
        from google.cloud import storage

    except Exception:  # noqa: BLE001
        raise click.ClickException(
            "Could not upload file to Google Storage. Could not import the Google Storage Python API via `from google.cloud import storage`.  Please check your installation or try running `pip install --upgrade google-cloud-storage`."
        )
    try:
        storage_client = storage.Client()
        bucket_obj = storage_client.bucket(bucket)
        blob = bucket_obj.blob(object_name)
        blob.upload_from_filename(file)
    except Exception as e:  # noqa: BLE001
        raise click.ClickException(
            f"Failed to upload the working directory to Google Cloud Storage. Error {repr(e)}"
            "Please validate you have exported cloud credentials with the correct write permissions and the intended bucket exists in your Cloud Storage account. "
            "If you do not desire to upload your working directory, please set your working directory to a public remote URI or remove the runtime_environment from you service yaml."
        ) from e


def _upload_file_to_s3(file: str, bucket: str, object_key: str):
    try:
        import boto3
    except Exception:  # noqa: BLE001
        raise click.ClickException(
            "Could not upload file to S3: Could not import the Amazon S3 Python API via `import boto3`.  Please check your installation or try running `pip install boto3`."
        )
    try:
        s3_client = boto3.client("s3")
        s3_client.upload_file(file, bucket, object_key)
    except Exception as e:  # noqa: BLE001
        raise click.ClickException(
            f"Failed to upload the working directory to S3. Error {repr(e)}"
            "Please validate you have exported cloud credentials with the correct write permissions and the intended bucket exists in your S3 account. "
            "If you do not desire to upload your working directory, please set your working directory to a public remote URI or remove the runtime_environment from you service yaml."
        ) from e


def _get_remote_storage_object_name(upload_path, upload_filename):
    # Strip leading slash, otherwise bucket will create a new directory called "/".
    object_name = os.path.join(urlparse(upload_path).path, upload_filename).lstrip("/")
    return object_name


def _upload_file_to_remote_storage(
    source_file: str, upload_path: str, upload_filename: str
):
    parsed_upload_path = urlparse(upload_path)
    service = parsed_upload_path.scheme
    bucket = parsed_upload_path.netloc
    object_name = _get_remote_storage_object_name(upload_path, upload_filename)
    if service == "s3":
        _upload_file_to_s3(source_file, bucket, object_key=object_name)
    if service == "gs":
        _upload_file_to_google_cloud_storage(
            source_file, bucket, object_name=object_name
        )

    final_uploaded_filepath = os.path.join(upload_path, upload_filename)
    try:
        from smart_open import open

        open(final_uploaded_filepath)
    except Exception as e:  # noqa: BLE001
        raise click.ClickException(
            f"Could not open uploaded file, maybe something went wrong while uploading: {e}."
        )

    return final_uploaded_filepath


def is_dir_remote_uri(working_dir: str) -> bool:
    parsed = urlparse(working_dir)
    if parsed.scheme:
        return True
    return False


def upload_and_rewrite_working_dir(
    runtime_env_json: Dict[str, Any],
    upload_file_to_remote_storage_fn: Callable[
        [str, str, str], str
    ] = _upload_file_to_remote_storage,
) -> Dict[str, Any]:
    """Upload a local working_dir and rewrite the working_dir field with the destination remote URI.

    After uploading, deletes the "upload_path" field because it is no longer used and is not a valid
    OSS runtime env field.
    """
    if runtime_env_json.get("working_dir", None) is None:
        return runtime_env_json

    working_dir = runtime_env_json["working_dir"]
    if is_dir_remote_uri(working_dir):
        # The working dir is a remote URI already
        return runtime_env_json

    upload_path = runtime_env_json["upload_path"]
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_zip_file_path = os.path.join(
            temp_dir, "anyscale_generated_working_dir.zip"
        )
        zip_directory(
            working_dir,
            excludes=runtime_env_json.get("excludes", []),
            output_path=temp_zip_file_path,
            # Ray requires remote Zip URIs to consist of a single top-level directory when unzipped.
            include_parent_dir=True,
        )

        hash_val = hashlib.md5(Path(temp_zip_file_path).read_bytes()).hexdigest()
        uploaded_zip_file_name = f"_anyscale_pkg_{hash_val}.zip"
        final_uploaded_filepath = upload_file_to_remote_storage_fn(
            temp_zip_file_path, upload_path, uploaded_zip_file_name,
        )

    final_runtime_env = runtime_env_json.copy()
    final_runtime_env["working_dir"] = final_uploaded_filepath
    del final_runtime_env["upload_path"]
    return final_runtime_env


def override_runtime_env_config(
    runtime_env: Optional[Dict[str, Any]],
    anyscale_api_client: DefaultApi,
    api_client: DefaultApi,
    workload_type: Workload,
    compute_config_id: Optional[str],
    log: BlockLogger,
) -> Optional[Dict[str, Any]]:
    """ Override working_dir and upload_path for runtime environment
    1. If workspace environment, autopopulate working_dir
    2. If runtime env or working_dir is None or working_dir is a remote_uri, return existing runtime_env
    3. If working_dir is local directory and upload path is defined, upload and rewrite working_dir
    4. If working_dir is local directory and upload path is not defined, infer upload path, upload working_dir, and rewrite working_dir
    """

    existing_runtime_env = runtime_env

    existing_runtime_env = autopopulate_working_dir_for_workspace(
        runtime_env=existing_runtime_env, log=log
    )

    # If runtime is None, return empty dict
    # Elif working_dir is missing, return existing runtime_env
    if not existing_runtime_env:
        return {}
    elif not existing_runtime_env.get("working_dir"):
        return existing_runtime_env

    working_dir = existing_runtime_env.get("working_dir", "")
    upload_path = existing_runtime_env.get("upload_path")

    if not is_dir_remote_uri(working_dir):
        if upload_path is not None:
            # If upload_path is specified
            # we back up the current working dir to the specified path
            new_runtime_env = upload_and_rewrite_working_dir(existing_runtime_env)
        else:
            if is_anyscale_workspace() and "ANYSCALE_SESSION_ID" in os.environ:
                # If submitting job v2 from workspaces and no upload_path is specified,
                # we back up the current workspace content into S3
                cluster_id = os.environ["ANYSCALE_SESSION_ID"]

                decorated_cluster = api_client.get_decorated_cluster_api_v2_decorated_sessions_cluster_id_get(
                    cluster_id
                ).result
                cloud_id = decorated_cluster.cloud.id

                workspace_id = os.environ["ANYSCALE_EXPERIMENTAL_WORKSPACE_ID"]

                new_runtime_env = infer_upload_path_and_rewrite_working_dir(
                    api_client=api_client,
                    existing_runtime_env=existing_runtime_env,
                    workload_type=workload_type,
                    cloud_id=cloud_id,
                    log=log,
                    workspace_id=workspace_id,
                )
            else:
                compute_template: ComputeTemplate = anyscale_api_client.get_compute_template(
                    compute_config_id
                ).result
                cloud_id = compute_template.config.cloud_id
                new_runtime_env = infer_upload_path_and_rewrite_working_dir(
                    api_client=api_client,
                    existing_runtime_env=existing_runtime_env,
                    workload_type=workload_type,
                    cloud_id=cloud_id,
                    log=log,
                )

        return new_runtime_env
    else:
        return existing_runtime_env


def autopopulate_working_dir_for_workspace(
    runtime_env: Optional[Dict[str, Any]], log: BlockLogger,
) -> Optional[Dict[str, Any]]:
    """Set the default working_dir to local directory if deploying from workspace
    """
    if is_anyscale_workspace():
        if not runtime_env:
            runtime_env = {}

        if not runtime_env.get("working_dir"):
            runtime_env["working_dir"] = "."
            log.info(
                "Working_dir is not specified, setting your current local directory as the working_dir"
            )

    return runtime_env


def infer_upload_path_and_rewrite_working_dir(
    *,
    api_client: DefaultApi,
    existing_runtime_env: Dict[str, Any],
    cloud_id: str,
    workload_type: Workload,
    log: BlockLogger,
    workspace_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Push working_dir to remote bucket and rewrite the working_dir field with the destination uri

    If the upload_path is not specified by the user, we will get the bucket name based on the cloud.
    We then rewrite the working_dir to the remote uri path
    so that the launched service will read from remote bucket directly.

    For Workspaces:
        The remote path: [s3, gs]://{bucket_name}/{org_id}/{cloud_id}/workspace_snapshots/{workspace_id}/{workload_type}/{backup_zip}
    Otherwise:
        The remote path: [s3, gs]://{bucket_name}/{org_id}/{cloud_id}/{workload_type}/{backup_zip}
        workload_type=[jobs, scheduled_jobs, services]
    """

    cloud: CloudWithCloudResource = api_client.get_cloud_with_cloud_resource_api_v2_clouds_with_cloud_resource_router_cloud_id_get(
        cloud_id
    ).result
    org_id = _get_organization_id(api_client)

    if cloud.provider == CloudProviders.AWS:
        bucket_name = _get_cloud_s3_bucket_from_cloud(cloud)
        protocol = "s3"
    elif cloud.provider == CloudProviders.GCP:
        bucket_name = _get_cloud_gs_bucket_from_cloud(api_client, cloud)
        protocol = "gs"
    else:
        raise click.ClickException(
            f"Currently launching a service from workspaces in a {cloud.provider} cloud is not supported. "
            "Please contact Anyscale support for more info."
        )

    new_runtime_env = copy.deepcopy(existing_runtime_env)
    pre_upload_working_dir = new_runtime_env["working_dir"]

    if workspace_id:
        new_runtime_env[
            "upload_path"
        ] = f"{protocol}://{bucket_name}/{org_id}/{cloud_id}/workspace_snapshots/{workspace_id}/{workload_type}"
    else:
        new_runtime_env[
            "upload_path"
        ] = f"{protocol}://{bucket_name}/{org_id}/{cloud_id}/{workload_type}"

    new_runtime_env = upload_and_rewrite_working_dir(new_runtime_env)

    log.info(
        f"Uploaded working directory content from {Path(pre_upload_working_dir).absolute()} to {new_runtime_env['working_dir']}"
    )
    return new_runtime_env


def _get_organization_id(api_client: DefaultApi):
    user_info: UserInfo = (api_client.get_user_info_api_v2_userinfo_get().result)
    orgs = user_info.organizations
    return orgs[0].id


def _get_cloud_s3_bucket_from_cloud(cloud: CloudWithCloudResource) -> Optional[str]:
    """
    If the cloud has an associated aws s3 bucket, we return its name.

    Please note that this is only for v2 clouds where customers have their
    own S3 buckets.
    """
    assert cloud.provider == CloudProviders.AWS
    if cloud and cloud.cloud_resource and cloud.cloud_resource.aws_s3_id:
        return bucket_name_from_maybe_bucket_arn(cloud.cloud_resource.aws_s3_id)
    else:
        return None


def _get_cloud_gs_bucket_from_cloud(
    api_client: DefaultApi, cloud: CloudWithCloudResource
) -> Optional[str]:
    """
    If the cloud has an associated Google Storage bucket, we return its name.

    Please note that this is only for v2 clouds where customers have their
    own Google Storage.
    """
    assert cloud.provider == CloudProviders.GCP

    gcp_cloud: CloudWithCloudResourceGCP = api_client.get_cloud_with_cloud_resource_api_v2_clouds_with_cloud_resource_gcp_router_cloud_id_get(
        cloud.id
    ).result

    if (
        gcp_cloud
        and gcp_cloud.cloud_resource
        and gcp_cloud.cloud_resource.gcp_cloud_storage_bucket_id
    ):
        gs_bucket_name = gcp_cloud.cloud_resource.gcp_cloud_storage_bucket_id
        return gs_bucket_name
    else:
        return None
