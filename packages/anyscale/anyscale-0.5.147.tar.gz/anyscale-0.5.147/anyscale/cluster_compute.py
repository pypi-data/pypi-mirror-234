from typing import Optional

from anyscale.authenticate import get_auth_api_client
from anyscale.cli_logger import BlockLogger
from anyscale.client.openapi_client.api.default_api import DefaultApi
from anyscale.cloud import get_cloud_id_and_name, get_last_used_cloud
from anyscale.sdk.anyscale_client import (
    ArchiveStatus,
    ComputeTemplateConfig,
    CreateComputeTemplate,
)
from anyscale.sdk.anyscale_client.models.cluster_compute_config import (
    ClusterComputeConfig,
)
from anyscale.sdk.anyscale_client.models.compute_template import ComputeTemplate
from anyscale.sdk.anyscale_client.models.compute_template_query import (
    ComputeTemplateQuery,
)
from anyscale.utils.cloud_utils import get_organization_default_cloud


log = BlockLogger()


def get_default_cluster_compute(
    cloud_name: Optional[str],
    project_id: Optional[str],
    api_client: Optional[DefaultApi] = None,
    anyscale_api_client: Optional[DefaultApi] = None,
) -> ComputeTemplate:
    if api_client is None:
        api_client = get_auth_api_client().api_client
    if anyscale_api_client is None:
        anyscale_api_client = get_auth_api_client().anyscale_api_client

    if cloud_name is None:
        default_cloud_name = get_organization_default_cloud(api_client)
        if default_cloud_name:
            cloud_name = default_cloud_name
        else:
            cloud_name = get_last_used_cloud(project_id, anyscale_api_client)

    cloud_id, _ = get_cloud_id_and_name(api_client, cloud_name=cloud_name)
    config_object = anyscale_api_client.get_default_compute_config(cloud_id).result
    compute_template = register_compute_template(config_object, api_client=api_client)
    return compute_template


def get_cluster_compute_from_name(
    cluster_compute_name: str,
    api_client: Optional[DefaultApi] = None,
    version: Optional[int] = None,
) -> ComputeTemplate:
    if api_client is None:
        api_client = get_auth_api_client().api_client
    cluster_computes = api_client.search_compute_templates_api_v2_compute_templates_search_post(
        ComputeTemplateQuery(
            orgwide=True,
            name={"equals": cluster_compute_name},
            include_anonymous=True,
            archive_status=ArchiveStatus.ALL,
            version=version,
        )
    ).results

    if len(cluster_computes) == 0:
        raise ValueError(
            f"The cluster compute template {cluster_compute_name} is not registered."
        )
    return cluster_computes[0]


def register_compute_template(
    config_object: ComputeTemplateConfig, api_client: Optional[DefaultApi] = None,
) -> ComputeTemplate:
    """
    Register compute template with a default name and return the compute template id."""
    if api_client is None:
        api_client = get_auth_api_client().api_client
    created_template = api_client.create_compute_template_api_v2_compute_templates_post(
        create_compute_template=CreateComputeTemplate(
            config=config_object, anonymous=True,
        )
    ).result
    return created_template


def get_selected_cloud_id_or_default(
    api_client: Optional[DefaultApi] = None,
    anyscale_api_client: Optional[DefaultApi] = None,
    cluster_compute_id: Optional[str] = None,
    cluster_compute_config: Optional[ClusterComputeConfig] = None,
    cloud_id: Optional[str] = None,
    cloud_name: Optional[str] = None,
):
    """
    Gets cloud_id that is selected for the current command from the
    arguments `cloud_id`, `cloud_name`, `cluster_compute_id`, or `cluster_compute_config`.
    If the cloud_id is not selected through any of these arguments, get the default cloud
    from the default cluster compute.
    """
    api_client = api_client or get_auth_api_client(log_output=False).api_client
    anyscale_api_client = (
        anyscale_api_client or get_auth_api_client(log_output=False).anyscale_api_client
    )
    if cloud_id or cloud_name:
        parent_cloud_id, _ = get_cloud_id_and_name(
            api_client=api_client, cloud_id=cloud_id, cloud_name=cloud_name,
        )
    elif cluster_compute_id:
        parent_cloud_id = anyscale_api_client.get_cluster_compute(
            cluster_compute_id
        ).result.config.cloud_id
    elif cluster_compute_config:
        parent_cloud_id = cluster_compute_config.cloud_id
    else:
        parent_cloud_id = (
            anyscale_api_client.get_default_cluster_compute().result.config.cloud_id
        )
    return parent_cloud_id
