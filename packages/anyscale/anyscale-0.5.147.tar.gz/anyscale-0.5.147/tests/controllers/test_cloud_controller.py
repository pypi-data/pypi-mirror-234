import json
from typing import Any, Dict, Iterator, List, Optional
from unittest.mock import ANY, MagicMock, Mock, patch

import boto3
from click import ClickException
from google.api_core.exceptions import NotFound
from google.auth.credentials import AnonymousCredentials
from moto import mock_acm, mock_cloudformation
import mypy_boto3_cloudformation.type_defs as cf_types
import pytest

from anyscale.client.openapi_client.models import (
    AWSMemoryDBClusterConfig,
    Cloud,
    CloudRegionAndZones,
    CloudregionandzonesResponse,
    CloudRegionInfo,
    CloudResponse,
    ClusterManagementStackVersions,
    CreateCloudResource,
    CreateCloudResourceGCP,
    EditableCloudResource,
    EditableCloudResourceGCP,
    UpdateCloudWithCloudResource,
    UpdateCloudWithCloudResourceGCP,
    WriteCloud,
)
from anyscale.client.openapi_client.models.cloud_state import CloudState
from anyscale.client.openapi_client.models.gcp_file_store_config import (
    GCPFileStoreConfig,
)
from anyscale.client.openapi_client.models.gcp_memorystore_instance_config import (
    GCPMemorystoreInstanceConfig,
)
from anyscale.client.openapi_client.models.subnet_id_with_availability_zone_aws import (
    SubnetIdWithAvailabilityZoneAWS,
)
from anyscale.controllers.cloud_controller import CloudController
from anyscale.utils.gcp_utils import GoogleCloudClientFactory
from frontend.cli.anyscale.controllers.cloud_functional_verification_controller import (
    CloudFunctionalVerificationType,
)


DEFAULT_RAY_IAM_ROLE = "ray-autoscaler-v1"


@pytest.fixture()
def mock_api_client(cloud_test_data: Cloud) -> Mock:
    mock_api_client = Mock()
    mock_api_client.get_cloud_api_v2_clouds_cloud_id_get = Mock(
        return_value=CloudResponse(result=cloud_test_data)
    )
    mock_api_client.find_cloud_by_name_api_v2_clouds_find_by_name_post = Mock(
        return_value=CloudResponse(result=cloud_test_data)
    )
    mock_api_client.delete_cloud_api_v2_clouds_cloud_id_delete = Mock(return_value={})
    mock_api_client.update_cloud_config_api_v2_clouds_cloud_id_config_put = Mock(
        return_value={}
    )
    mock_api_client.get_regions_and_zones_api_v2_clouds_gcp_regions_and_zones_get = Mock(
        return_value=CloudregionandzonesResponse(
            result=CloudRegionAndZones(
                regions={
                    "us-west1": CloudRegionInfo(name="us-west1", availability_zones={}),
                    "us-west2": CloudRegionInfo(name="us-west2", availability_zones={}),
                }
            )
        )
    )

    return mock_api_client


@pytest.fixture(autouse=True)
def mock_auth_api_client(
    mock_api_client: Mock, base_mock_anyscale_api_client: Mock
) -> Iterator[None]:
    mock_auth_api_client = Mock(
        api_client=mock_api_client, anyscale_api_client=base_mock_anyscale_api_client,
    )
    with patch.multiple(
        "anyscale.controllers.base_controller",
        get_auth_api_client=Mock(return_value=mock_auth_api_client),
    ):
        yield


@pytest.fixture(autouse=True)
def mock_get_available_regions() -> Iterator[None]:
    with patch(
        "anyscale.controllers.cloud_controller.get_available_regions",
        return_value=["us-west-2"],
        autospec=True,
    ):
        yield


def mock_role(document: Optional[Dict[str, Any]] = None) -> Mock:
    if document is None:
        document = {}
    mock_role = Mock()

    mock_role.arn = "ARN"
    mock_role.attach_policy = Mock()
    mock_role.assume_role_policy_document = document
    mock_role.instance_profiles.all = Mock(return_value=[])

    return mock_role


def mock_role_with_external_id() -> Mock:
    return mock_role(
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "1",
                    "Effect": "Allow",
                    "Principal": {"AWS": ["ARN"]},
                    "Action": "sts:AssumeRole",
                    "Condition": {"StringEquals": {"sts:ExternalId": "extid"}},
                }
            ],
        }
    )


def test_delete_cloud_by_name(cloud_test_data: Cloud) -> None:
    cloud_controller = CloudController()
    success = cloud_controller.delete_cloud(
        cloud_id=None, cloud_name=cloud_test_data.name, skip_confirmation=True
    )
    assert success

    cloud_controller.api_client.find_cloud_by_name_api_v2_clouds_find_by_name_post.assert_called_once_with(
        cloud_name_options={"name": cloud_test_data.name}
    )
    cloud_controller.api_client.delete_cloud_api_v2_clouds_cloud_id_delete(
        cloud_id=cloud_test_data.id
    )


def test_delete_cloud_by_id(cloud_test_data: Cloud) -> None:
    cloud_controller = CloudController()
    success = cloud_controller.delete_cloud(
        cloud_id=cloud_test_data.id, cloud_name=None, skip_confirmation=True
    )
    assert success

    cloud_controller.api_client.get_cloud_api_v2_clouds_cloud_id_get.assert_called_with(
        cloud_id=cloud_test_data.id
    )
    cloud_controller.api_client.delete_cloud_api_v2_clouds_cloud_id_delete(
        cloud_id=cloud_test_data.id
    )


def test_missing_name_and_id() -> None:
    cloud_controller = CloudController()

    with pytest.raises(ClickException):
        cloud_controller.delete_cloud(None, None, True)

    with pytest.raises(ClickException):
        cloud_controller.update_managed_cloud(None, None, False, None, True)

    with pytest.raises(ClickException):
        cloud_controller.get_cloud_config(None, None)


def test_prepare_for_managed_cloud_setup() -> None:
    mock_get_available_regions = Mock(return_value=["us-west-1", "us-west-2"])
    mock_get_role = Mock(return_value=None)
    mock_get_user_env_aws_account = Mock(return_value="mock_user_aws_account_id")
    mock_create_cloud_api_v2_clouds_post = Mock(
        return_value=Mock(result=Mock(id="mock_cloud_id"))
    )
    cluster_management_stack_version = ClusterManagementStackVersions.V2

    with patch.multiple(
        "anyscale.controllers.cloud_controller",
        get_available_regions=mock_get_available_regions,
        _get_role=mock_get_role,
        get_user_env_aws_account=mock_get_user_env_aws_account,
    ), patch.multiple("secrets", token_hex=Mock(return_value="02e38860")):
        cloud_controller = CloudController()
        cloud_controller.api_client.create_cloud_api_v2_clouds_post = (
            mock_create_cloud_api_v2_clouds_post
        )

        (
            anyscale_iam_role_name,
            created_cloud_id,
        ) = cloud_controller.prepare_for_managed_cloud_setup(
            "us-west-2", "cloud_name", cluster_management_stack_version
        )

    assert anyscale_iam_role_name == "anyscale-iam-role-02e38860"
    assert created_cloud_id == "mock_cloud_id"

    mock_get_available_regions.assert_called_once_with()
    mock_get_role.assert_called_once_with(anyscale_iam_role_name, "us-west-2")
    mock_get_user_env_aws_account.assert_called_once_with("us-west-2")
    mock_create_cloud_api_v2_clouds_post.assert_called_once_with(
        write_cloud=WriteCloud(
            provider="AWS",
            region="us-west-2",
            credentials=f"arn:aws:iam::mock_user_aws_account_id:role/{anyscale_iam_role_name}",
            name="cloud_name",
            is_bring_your_own_resource=False,
            cluster_management_stack_version=cluster_management_stack_version,
        )
    )


@pytest.mark.parametrize(
    ("permission_denied", "no_available_token", "cloud_creation_failed"),
    [
        pytest.param(False, False, False, id="success",),
        pytest.param(True, False, False, id="permission-denied",),
        pytest.param(False, True, False, id="no-token",),
        pytest.param(False, False, True, id="cloud-creation-failed",),
    ],
)
def test_prepare_for_managed_cloud_setup_gcp(
    permission_denied: bool, no_available_token: bool, cloud_creation_failed: bool
) -> None:
    cluster_management_stack_version = ClusterManagementStackVersions.V2
    factory = Mock()
    mock_token_hex = "02e38860"
    mock_project_id = "mock-project-id"
    mock_project_number = "123456789"
    mock_cloud_id = "mock_cloud_id"
    mock_cloud_name = "mock_cloud_name"
    mock_region = "us-west1"
    mock_pool_name = f"projects/{mock_project_number}/locations/global/workloadIdentityPools/anyscale-provider-pool-{mock_token_hex}"
    mock_service_account_email = (
        f"anyscale-access-{mock_token_hex}@{mock_project_id}.iam.gserviceaccount.com"
    )
    setup_utils_mock = Mock()
    setup_utils_mock.get_anyscale_gcp_access_service_acount = Mock(return_value=None)
    setup_utils_mock.get_workload_identity_pool = Mock(return_value=None)

    setup_utils_mock.get_project_number = Mock(
        return_value=f"projects/{mock_project_number}"
    )

    if cloud_creation_failed:
        mock_create_cloud_api_v2_clouds_post = Mock(side_effect=ClickException("409"))
    else:
        mock_create_cloud_api_v2_clouds_post = Mock(
            return_value=Mock(result=Mock(id=mock_cloud_id))
        )

    if permission_denied:
        with patch.multiple(
            "anyscale.controllers.cloud_controller",
            try_import_gcp_managed_setup_utils=Mock(return_value=setup_utils_mock),
        ), patch.multiple(
            "secrets", token_hex=Mock(side_effect=mock_token_hex)
        ), pytest.raises(
            ClickException
        ):
            setup_utils_mock.get_anyscale_gcp_access_service_acount = Mock(
                side_effect=ClickException("Failed to get")
            )
            setup_utils_mock.get_workload_identity_pool = Mock(
                side_effect=ClickException("Failed to get")
            )
            CloudController().prepare_for_managed_cloud_setup_gcp(
                mock_project_id,
                mock_region,
                mock_cloud_name,
                factory,
                cluster_management_stack_version,
            )
            setup_utils_mock.get_anyscale_gcp_access_service_acount.assert_called_once_with(
                factory, mock_service_account_email
            )
            setup_utils_mock.get_workload_identity_pool.assert_not_called()
    elif no_available_token:
        with patch.multiple(
            "anyscale.controllers.cloud_controller",
            try_import_gcp_managed_setup_utils=Mock(return_value=setup_utils_mock),
        ), patch.multiple(
            "secrets", token_hex=Mock(side_effect=["a", "b", "c", "d", "e"])
        ), pytest.raises(
            ClickException
        ) as e:
            setup_utils_mock.get_anyscale_gcp_access_service_acount = Mock(
                return_value="something"
            )
            setup_utils_mock.get_workload_identity_pool = Mock(return_value="something")

            CloudController().prepare_for_managed_cloud_setup_gcp(
                mock_project_id,
                mock_region,
                mock_cloud_name,
                factory,
                cluster_management_stack_version,
            )
        e.match(
            "we weren't able to find an available service account name and create a provider pool in your GCP project."
        )

        assert setup_utils_mock.get_anyscale_gcp_access_service_acount.call_count == 5
        setup_utils_mock.get_workload_identity_pool.assert_not_called()

    elif cloud_creation_failed:
        with patch.multiple(
            "anyscale.controllers.cloud_controller",
            try_import_gcp_managed_setup_utils=Mock(return_value=setup_utils_mock),
        ), patch.multiple(
            "secrets", token_hex=Mock(return_value=mock_token_hex)
        ), pytest.raises(
            ClickException
        ) as e:
            cloud_controller = CloudController()
            cloud_controller.api_client.create_cloud_api_v2_clouds_post = (
                mock_create_cloud_api_v2_clouds_post
            )

            cloud_controller.prepare_for_managed_cloud_setup_gcp(
                mock_project_id,
                mock_region,
                mock_cloud_name,
                factory,
                cluster_management_stack_version,
            )
        e.match("already exists. Please choose a different name.")

        setup_utils_mock.get_anyscale_gcp_access_service_acount.assert_called_once_with(
            factory, mock_service_account_email
        )
        setup_utils_mock.get_workload_identity_pool.assert_called_once_with(
            factory, mock_project_id, mock_pool_name.split("/")[-1]
        )
        mock_create_cloud_api_v2_clouds_post.assert_called_once_with(
            write_cloud=WriteCloud(
                provider="GCP",
                region=mock_region,
                credentials=json.dumps(
                    {
                        "project_id": mock_project_id,
                        "provider_id": f"{mock_pool_name}/providers/anyscale-access",
                        "service_account_email": mock_service_account_email,
                    }
                ),
                name=mock_cloud_name,
                is_bring_your_own_resource=False,
                cluster_management_stack_version=cluster_management_stack_version,
            )
        )
    else:
        # success path
        with patch.multiple(
            "anyscale.controllers.cloud_controller",
            try_import_gcp_managed_setup_utils=Mock(return_value=setup_utils_mock),
        ), patch.multiple("secrets", token_hex=Mock(return_value=mock_token_hex)):
            cloud_controller = CloudController()
            cloud_controller.api_client.create_cloud_api_v2_clouds_post = (
                mock_create_cloud_api_v2_clouds_post
            )

            (
                chosen_anyscale_admin_service_account,
                chosen_pool_name,
                created_cloud_id,
            ) = cloud_controller.prepare_for_managed_cloud_setup_gcp(
                mock_project_id,
                mock_region,
                mock_cloud_name,
                factory,
                cluster_management_stack_version,
            )

        assert chosen_pool_name == mock_pool_name
        assert chosen_anyscale_admin_service_account == mock_service_account_email
        assert created_cloud_id == mock_cloud_id

        setup_utils_mock.get_anyscale_gcp_access_service_acount.assert_called_once_with(
            factory, mock_service_account_email
        )
        setup_utils_mock.get_workload_identity_pool.assert_called_once_with(
            factory, mock_project_id, mock_pool_name.split("/")[-1]
        )
        mock_create_cloud_api_v2_clouds_post.assert_called_once_with(
            write_cloud=WriteCloud(
                provider="GCP",
                region=mock_region,
                credentials=json.dumps(
                    {
                        "project_id": mock_project_id,
                        "provider_id": f"{mock_pool_name}/providers/anyscale-access",
                        "service_account_email": mock_service_account_email,
                    }
                ),
                name=mock_cloud_name,
                is_bring_your_own_resource=False,
                cluster_management_stack_version=cluster_management_stack_version,
            )
        )


@pytest.mark.parametrize(
    ("create_pool_failed", "create_provider_failed"),
    [
        pytest.param(False, False, id="success",),
        pytest.param(True, False, id="create-pool-failed",),
        pytest.param(False, True, id="create-provider-failed",),
    ],
)
def test_create_workload_identity_federation_provider(
    create_pool_failed: bool, create_provider_failed: bool
):
    setup_utils_mock = Mock()

    factory = Mock()
    mock_project_id = "mock-project-id"
    mock_pool_id = "mock-pool-id"
    mock_service_account = "mock@mock-project-id.iam.gserviceaccount.com"
    mock_project_number = "projects/112233445566"
    mock_pool_name = (
        f"{mock_project_number}/locations/global/workloadIdentityPools/{mock_pool_id}"
    )

    mock_anyscale_aws_account = "123456"
    mock_org_id = "mock_org_id"
    mock_get_anyscale_aws_account_api_v2_clouds_anyscale_aws_account_get = Mock(
        return_value=Mock(result=Mock(anyscale_aws_account=mock_anyscale_aws_account))
    )
    if create_pool_failed:
        with patch.multiple(
            "anyscale.controllers.cloud_controller",
            try_import_gcp_managed_setup_utils=Mock(return_value=setup_utils_mock),
            get_organization_id=Mock(return_value=mock_org_id),
        ), pytest.raises(ClickException):
            setup_utils_mock.create_workload_identity_pool = Mock(
                side_effect=ClickException("error")
            )

            cloud_controller = CloudController()
            cloud_controller.create_workload_identity_federation_provider(
                factory, mock_project_id, mock_pool_id, mock_service_account
            )

            setup_utils_mock.create_workload_identity_pool.assert_called_once_with(
                factory,
                mock_project_id,
                mock_pool_id,
                cloud_controller.log,
                "Anyscale provider pool",
                f"Workload Identity Provider Pool for Anyscale access service account {mock_service_account}",
            )
            setup_utils_mock.create_anyscale_aws_provider.assert_not_called()
    elif create_provider_failed:
        with patch.multiple(
            "anyscale.controllers.cloud_controller",
            try_import_gcp_managed_setup_utils=Mock(return_value=setup_utils_mock),
            get_organization_id=Mock(return_value=mock_org_id),
        ), pytest.raises(ClickException) as e:
            setup_utils_mock.create_workload_identity_pool = Mock(
                return_value=mock_pool_name
            )
            setup_utils_mock.create_anyscale_aws_provider = Mock(
                side_effect=ClickException("error")
            )
            setup_utils_mock.delete_workload_identity_pool = Mock()

            cloud_controller = CloudController()
            cloud_controller.api_client.get_anyscale_aws_account_api_v2_clouds_anyscale_aws_account_get = (
                mock_get_anyscale_aws_account_api_v2_clouds_anyscale_aws_account_get
            )
            cloud_controller.create_workload_identity_federation_provider(
                factory, mock_project_id, mock_pool_id, mock_service_account
            )

        setup_utils_mock.create_workload_identity_pool.assert_called_once_with(
            factory,
            mock_project_id,
            mock_pool_id,
            cloud_controller.log,
            "Anyscale provider pool",
            f"Workload Identity Provider Pool for Anyscale access service account {mock_service_account}",
        )
        setup_utils_mock.create_anyscale_aws_provider.assert_called_once_with(
            factory,
            mock_org_id,
            mock_pool_name,
            "anyscale-access",
            mock_anyscale_aws_account,
            "Anyscale Access",
            cloud_controller.log,
        )
        e.match("Error occurred when trying to set up workload identity federation")
    else:
        # succeed path
        with patch.multiple(
            "anyscale.controllers.cloud_controller",
            try_import_gcp_managed_setup_utils=Mock(return_value=setup_utils_mock),
            get_organization_id=Mock(return_value=mock_org_id),
        ):
            setup_utils_mock.create_workload_identity_pool = Mock(
                return_value=mock_pool_name
            )
            setup_utils_mock.create_anyscale_aws_provider = Mock()

            cloud_controller = CloudController()
            cloud_controller.api_client.get_anyscale_aws_account_api_v2_clouds_anyscale_aws_account_get = (
                mock_get_anyscale_aws_account_api_v2_clouds_anyscale_aws_account_get
            )
            cloud_controller.create_workload_identity_federation_provider(
                factory, mock_project_id, mock_pool_id, mock_service_account
            )

            setup_utils_mock.create_workload_identity_pool.assert_called_once_with(
                factory,
                mock_project_id,
                mock_pool_id,
                cloud_controller.log,
                "Anyscale provider pool",
                f"Workload Identity Provider Pool for Anyscale access service account {mock_service_account}",
            )
            setup_utils_mock.create_anyscale_aws_provider.assert_called_once_with(
                factory,
                mock_org_id,
                mock_pool_name,
                "anyscale-access",
                mock_anyscale_aws_account,
                "Anyscale Access",
                cloud_controller.log,
            )


@pytest.mark.parametrize("cloud_id", [None, "cloud_id_1"])
@pytest.mark.parametrize("cloud_name", [None, "cloud_name_1"])
def test_set_default_cloud(cloud_id: Optional[str], cloud_name: Optional[str]) -> None:
    cloud_controller = CloudController()
    if not (cloud_id or cloud_name) or (cloud_id and cloud_name):
        # Error if neither or both of cloud_id and cloud_name provided
        with pytest.raises(ClickException):
            cloud_controller.set_default_cloud(
                cloud_id=cloud_id, cloud_name=cloud_name,
            )
    else:
        cloud_controller.set_default_cloud(
            cloud_id=cloud_id, cloud_name=cloud_name,
        )
        cloud_controller.api_client.update_default_cloud_api_v2_organizations_update_default_cloud_post.assert_called_once_with(
            cloud_id="cloud_id_1"
        )


@pytest.mark.parametrize("cloud_id", [None, "cloud_id_1"])
@pytest.mark.parametrize("cloud_name", [None, "cloud_name_1"])
def test_list_cloud(cloud_id: Optional[str], cloud_name: Optional[str]) -> None:
    cloud_controller = CloudController()
    cloud_controller.api_client.list_clouds_api_v2_clouds_get = Mock(
        return_value=Mock(results=[Mock()])
    )
    cloud_controller.list_clouds(cloud_name, cloud_id)

    if cloud_id is not None:
        cloud_controller.api_client.get_cloud_api_v2_clouds_cloud_id_get.assert_called_once_with(
            cloud_id
        )
    elif cloud_name is not None:
        cloud_controller.api_client.find_cloud_by_name_api_v2_clouds_find_by_name_post.assert_called_once_with(
            {"name": cloud_name}
        )
    else:
        cloud_controller.api_client.list_clouds_api_v2_clouds_get.assert_called_once_with()


@pytest.mark.parametrize(
    "anyscale_iam_role",
    [
        "arn:aws:iam::123:role/mock_anyscale_role",
        "arn:aws:iam::123:role/path/mock_anyscale_role",
    ],
)
@pytest.mark.parametrize(
    "anyscale_instance_role",
    [
        "arn:aws:iam::123:role/instance_role",
        "arn:aws:iam::123:role/path/instance_role",
    ],
)
@pytest.mark.parametrize("verify_success", [True, False])
@pytest.mark.parametrize("private_network", [True, False])
@pytest.mark.parametrize("enable_head_node_fault_tolerance", [True, False])
def test_register_cloud_aws(
    anyscale_iam_role: str,
    anyscale_instance_role: str,
    verify_success: bool,
    private_network: bool,
    enable_head_node_fault_tolerance: bool,
) -> None:

    mock_cloud = Mock(result=Mock(id="mock_cloud_id"))
    mock_api_client = Mock(
        create_cloud_api_v2_clouds_post=Mock(return_value=mock_cloud)
    )
    mock_region = "mock_region"
    mock_cloud_name = "mock_cloud"
    mock_vpc_id = "mock_vpc_id"
    mock_subnet_ids = ["mock_subnet"]
    mock_efs_id = "mock_efs_id"
    mock_security_group_ids = ["security_group_id"]
    mock_s3_bucket_id = "mock_s3_bucket_id"
    mock_get_role = Mock()
    mock_get_aws_efs_mount_target_ip = Mock(return_value="mock_efs_ip")
    mock_memorydb_cluster_id = (
        "mock_memorydb_cluster_id" if enable_head_node_fault_tolerance else None
    )

    if enable_head_node_fault_tolerance:
        mock_memorydb_cluster_config = AWSMemoryDBClusterConfig(
            id=mock_memorydb_cluster_id, endpoint="mock-endpoint:6379"
        )
    else:
        mock_memorydb_cluster_config = None

    mock_get_memorydb_cluster_config = Mock(return_value=mock_memorydb_cluster_config)

    def mock_associate_subnet_ids_with_policy(resource, region, logger):
        return [SubnetIdWithAvailabilityZoneAWS("mock_subnet", "mock_az")]

    cluster_management_stack_version = ClusterManagementStackVersions.V2
    with patch(
        "anyscale.controllers.cloud_controller.CloudController.verify_aws_cloud_resources",
        new=Mock(return_value=verify_success),
    ), patch.multiple(
        "anyscale.controllers.cloud_controller",
        associate_aws_subnets_with_azs=mock_associate_subnet_ids_with_policy,
        _update_external_ids_for_policy=Mock(return_value={"mock_policy": "test"}),
        _get_role=mock_get_role,
        _get_aws_efs_mount_target_ip=mock_get_aws_efs_mount_target_ip,
        _get_memorydb_cluster_config=mock_get_memorydb_cluster_config,
    ):
        cloud_controller = CloudController()
        cloud_controller.api_client = mock_api_client

        if verify_success:
            cloud_controller.register_aws_cloud(
                region=mock_region,
                name=mock_cloud_name,
                vpc_id=mock_vpc_id,
                subnet_ids=mock_subnet_ids,
                efs_id=mock_efs_id,
                anyscale_iam_role_id=anyscale_iam_role,
                instance_iam_role_id=anyscale_instance_role,
                security_group_ids=mock_security_group_ids,
                s3_bucket_id=mock_s3_bucket_id,
                memorydb_cluster_id=mock_memorydb_cluster_id,
                functional_verify=None,
                private_network=private_network,
                cluster_management_stack_version=cluster_management_stack_version,
                yes=True,
            )
        else:
            with pytest.raises(ClickException) as e:
                cloud_controller.register_aws_cloud(
                    region=mock_region,
                    name=mock_cloud_name,
                    vpc_id=mock_vpc_id,
                    subnet_ids=mock_subnet_ids,
                    efs_id=mock_efs_id,
                    anyscale_iam_role_id=anyscale_iam_role,
                    instance_iam_role_id=anyscale_instance_role,
                    security_group_ids=mock_security_group_ids,
                    s3_bucket_id=mock_s3_bucket_id,
                    memorydb_cluster_id=mock_memorydb_cluster_id,
                    functional_verify=None,
                    private_network=private_network,
                    cluster_management_stack_version=cluster_management_stack_version,
                    yes=True,
                )
            e.match("Please make sure all the resources provided")
    mock_get_role.assert_called_once_with("mock_anyscale_role", mock_region)

    mock_api_client.create_cloud_api_v2_clouds_post.assert_called_with(
        write_cloud=WriteCloud(
            provider="AWS",
            region=mock_region,
            credentials=anyscale_iam_role,
            name=mock_cloud_name,
            is_bring_your_own_resource=True,
            is_private_cloud=private_network,
            cluster_management_stack_version=cluster_management_stack_version,
        )
    )

    mock_subnet_ids_with_azs = mock_associate_subnet_ids_with_policy(
        mock_subnet_ids, mock_region, Mock()
    )

    if verify_success:
        mock_api_client.update_cloud_with_cloud_resource_api_v2_clouds_with_cloud_resource_router_cloud_id_put.assert_called_with(
            cloud_id=mock_cloud.result.id,
            update_cloud_with_cloud_resource=UpdateCloudWithCloudResource(
                cloud_resource_to_update=CreateCloudResource(
                    aws_vpc_id=mock_vpc_id,
                    aws_subnet_ids_with_availability_zones=mock_subnet_ids_with_azs,
                    aws_iam_role_arns=[anyscale_iam_role, anyscale_instance_role],
                    aws_security_groups=mock_security_group_ids,
                    aws_s3_id=mock_s3_bucket_id,
                    aws_efs_id=mock_efs_id,
                    aws_efs_mount_target_ip="mock_efs_ip",
                    memorydb_cluster_config=mock_memorydb_cluster_config,
                ),
            ),
        )
    else:
        mock_api_client.delete_cloud_api_v2_clouds_cloud_id_delete.assert_called_once_with(
            cloud_id=mock_cloud.result.id
        )


@pytest.mark.parametrize(
    ("valid_filestore_config", "verify_success"),
    [
        pytest.param(True, True, id="success",),
        pytest.param(True, False, id="verification-fails",),
        pytest.param(False, False, id="invalid-filestore",),
    ],
)
@pytest.mark.parametrize("private_network", [True, False])
@pytest.mark.parametrize("enable_head_node_fault_tolerance", [True, False])
def test_register_cloud_gcp(
    valid_filestore_config: bool,
    verify_success: bool,
    private_network: bool,
    enable_head_node_fault_tolerance: bool,
) -> None:
    mock_cloud = Mock(result=Mock(id="mock_cloud_id"))
    mock_api_client = Mock(
        create_cloud_api_v2_clouds_post=Mock(return_value=mock_cloud)
    )
    mock_region = "mock_region"
    mock_project_id = "mock_project_id"
    mock_cloud_name = "mock_cloud"
    mock_vpc_name = "mock_vpc_name"
    mock_subnet_names = ["mock_subnet"]
    mock_filestore_instance_id = "mock_filestore_instance"
    mock_filestore_location = "mock_filestore_location"
    mock_anyscale_service_account_email = "123@123.com"
    mock_instance_service_account_email = "456@456.com"
    mock_firewall_policy_names = ["mock_firewall_policy"]
    mock_cloud_storage_bucket_name = "mock_cloud_storage_bucket_name"
    mock_provider_id = "projects/123/locations/global/workloadIdentityPools/mock-pool/providers/mock-provider"
    mock_memorystore_instance_name = (
        "project/123/locations/global/instances/mock-memorystore-instance"
        if enable_head_node_fault_tolerance
        else None
    )
    cluster_management_stack_version = ClusterManagementStackVersions.V2

    def mock_get_gcp_filestore_config(
        factory, project_id, vpc_name, filestore_location, filestore_instance_id, logger
    ):
        if valid_filestore_config:
            return GCPFileStoreConfig(
                instance_name="mock_instance",
                mount_target_ip="mock_ip",
                root_dir="mock_root_dir",
            )
        else:
            raise NotFound

    gcp_utils_mock = Mock()
    gcp_utils_mock.get_google_cloud_client_factory = Mock(
        return_value=GoogleCloudClientFactory(credentials=AnonymousCredentials())
    )
    gcp_utils_mock.get_gcp_filestore_config = mock_get_gcp_filestore_config

    if enable_head_node_fault_tolerance:
        mock_gcp_memorystore_config = GCPMemorystoreInstanceConfig(
            name=mock_memorystore_instance_name, endpoint="mock_endpoint:1234"
        )
    else:
        mock_gcp_memorystore_config = None

    gcp_utils_mock.get_gcp_memorystore_config = Mock(
        return_value=mock_gcp_memorystore_config
    )

    with patch(
        "anyscale.controllers.cloud_controller.CloudController.verify_gcp_cloud_resources",
        new=Mock(return_value=verify_success),
    ), patch.multiple(
        "anyscale.controllers.cloud_controller",
        try_import_gcp_utils=Mock(return_value=gcp_utils_mock),
    ):
        cloud_controller = CloudController()
        cloud_controller.api_client = mock_api_client

        if verify_success:
            cloud_controller.register_gcp_cloud(
                region=mock_region,
                name=mock_cloud_name,
                project_id=mock_project_id,
                vpc_name=mock_vpc_name,
                subnet_names=mock_subnet_names,
                filestore_instance_id=mock_filestore_instance_id,
                filestore_location=mock_filestore_location,
                anyscale_service_account_email=mock_anyscale_service_account_email,
                instance_service_account_email=mock_instance_service_account_email,
                provider_id=mock_provider_id,
                firewall_policy_names=mock_firewall_policy_names,
                cloud_storage_bucket_name=mock_cloud_storage_bucket_name,
                memorystore_instance_name=mock_memorystore_instance_name,
                functional_verify=None,
                private_network=private_network,
                cluster_management_stack_version=cluster_management_stack_version,
                yes=True,
            )
        else:
            with pytest.raises(ClickException) as e:
                cloud_controller.register_gcp_cloud(
                    region=mock_region,
                    name=mock_cloud_name,
                    project_id=mock_project_id,
                    vpc_name=mock_vpc_name,
                    subnet_names=mock_subnet_names,
                    filestore_instance_id=mock_filestore_instance_id,
                    filestore_location=mock_filestore_location,
                    anyscale_service_account_email=mock_anyscale_service_account_email,
                    instance_service_account_email=mock_instance_service_account_email,
                    provider_id=mock_provider_id,
                    firewall_policy_names=mock_firewall_policy_names,
                    cloud_storage_bucket_name=mock_cloud_storage_bucket_name,
                    memorystore_instance_name=mock_memorystore_instance_name,
                    functional_verify=None,
                    private_network=private_network,
                    cluster_management_stack_version=cluster_management_stack_version,
                    yes=True,
                )
            if valid_filestore_config:
                e.match("Please make sure all the resources provided")

    mock_api_client.create_cloud_api_v2_clouds_post.assert_called_with(
        write_cloud=WriteCloud(
            provider="GCP",
            region=mock_region,
            credentials=json.dumps(
                {
                    "project_id": mock_project_id,
                    "provider_id": mock_provider_id,
                    "service_account_email": mock_anyscale_service_account_email,
                }
            ),
            name=mock_cloud_name,
            is_bring_your_own_resource=True,
            is_private_cloud=private_network,
            cluster_management_stack_version=cluster_management_stack_version,
        )
    )

    if verify_success:
        mock_api_client.update_cloud_with_cloud_resource_api_v2_clouds_with_cloud_resource_gcp_router_cloud_id_put.assert_called_with(
            cloud_id=mock_cloud.result.id,
            update_cloud_with_cloud_resource_gcp=UpdateCloudWithCloudResourceGCP(
                cloud_resource_to_update=CreateCloudResourceGCP(
                    gcp_vpc_id=mock_vpc_name,
                    gcp_subnet_ids=mock_subnet_names,
                    gcp_cluster_node_service_account_email=mock_instance_service_account_email,
                    gcp_anyscale_iam_service_account_email=mock_anyscale_service_account_email,
                    gcp_filestore_config=GCPFileStoreConfig(
                        instance_name="mock_instance",
                        mount_target_ip="mock_ip",
                        root_dir="mock_root_dir",
                    ),
                    gcp_firewall_policy_ids=mock_firewall_policy_names,
                    gcp_cloud_storage_bucket_id=mock_cloud_storage_bucket_name,
                    memorystore_instance_config=mock_gcp_memorystore_config,
                ),
            ),
        )
    else:
        mock_api_client.delete_cloud_api_v2_clouds_cloud_id_delete.assert_called_once_with(
            cloud_id=mock_cloud.result.id
        )


@pytest.mark.parametrize("state", [CloudState.ACTIVE, CloudState.DELETED])
@pytest.mark.parametrize("has_cloud_resource", [True, False])
@pytest.mark.parametrize("cloud_provider", ["AWS", "GCP"])
@pytest.mark.parametrize("is_bring_your_own_resource", [True, False])
def test_verify_cloud(
    state: CloudState,
    has_cloud_resource: bool,
    cloud_provider: str,
    is_bring_your_own_resource: bool,
):
    cloud_resource_mock = Mock() if has_cloud_resource else None
    verify_mock = Mock(return_value=True)
    verify_gcp_cloud_resources_mock = Mock(return_value=True)
    mock_project_id = "mock_project"  # for gcp clouds
    mock_cloud_id = "mock_cloud_id"
    mock_cloud_name = "mock_cloud_name"
    verify_aws_subnets_mock = Mock(return_value=True)
    with patch.multiple(
        "anyscale.controllers.cloud_controller",
        get_cloud_id_and_name=Mock(return_value=(mock_cloud_id, mock_cloud_name)),
        get_cloud_resource_by_cloud_id=Mock(return_value=cloud_resource_mock),
        verify_aws_vpc=verify_mock,
        verify_aws_subnets=verify_aws_subnets_mock,
        verify_aws_iam_roles=verify_mock,
        verify_aws_security_groups=verify_mock,
        verify_aws_s3=verify_mock,
        verify_aws_efs=verify_mock,
        verify_aws_cloudformation_stack=verify_mock,
        verify_aws_memorydb_cluster=verify_mock,
        CreateCloudResource=Mock(return_value=cloud_resource_mock),
    ), patch(
        "anyscale.controllers.cloud_controller.CloudController.verify_gcp_cloud_resources"
    ) as verify_gcp_cloud_resources_mock:
        cloud_controller = CloudController()
        cloud_controller.log = Mock()

        cloud = Mock(
            result=Mock(
                state=state,
                region="mock_region",
                credentials=json.dumps(
                    {"project_id": mock_project_id}
                ),  # for GCP clouds
                provider=cloud_provider,
                is_bring_your_own_resource=is_bring_your_own_resource,
                is_private_cloud=False,
                is_private_service_cloud=False,
            )
        )
        cloud_controller.api_client.get_cloud_api_v2_clouds_cloud_id_get = Mock(
            return_value=cloud
        )

        cloud_controller.api_client.get_cloud_with_cloud_resource_api_v2_clouds_with_cloud_resource_gcp_router_cloud_id_get = Mock(
            return_value=cloud
        )
        verify_result = cloud_controller.verify_cloud(
            cloud_name="mock_cloud_name",
            cloud_id="mock_cloud_id",
            functional_verify=None,
        )

        if state in (CloudState.DELETING, CloudState.DELETED):
            assert verify_result is False
        elif not has_cloud_resource:
            assert verify_result is False
        elif cloud_provider == "AWS":
            if is_bring_your_own_resource:
                assert verify_mock.call_count == 6
            else:
                assert verify_mock.call_count == 7
            verify_mock.assert_called_with(
                cloud_resource=cloud_resource_mock,
                boto3_session=ANY,
                logger=cloud_controller.log,
                strict=False,
            )
            verify_aws_subnets_mock.assert_called_once_with(
                cloud_resource=cloud_resource_mock,
                region=cloud.result.region,
                is_private_network=False,
                logger=cloud_controller.log,
                ignore_capacity_errors=False,
                strict=False,
            )
            assert verify_result
        elif cloud_provider == "GCP":
            verify_gcp_cloud_resources_mock.assert_called_once_with(
                cloud_resource=cloud_resource_mock,
                project_id=mock_project_id,
                region=cloud.result.region,
                cloud_id=mock_cloud_id,
                yes=False,
                strict=False,
                is_private_service_cloud=False,
            )
            assert verify_result


@pytest.mark.parametrize("cloud_setup_failure", [True, False])
@pytest.mark.parametrize("enable_head_node_fault_tolerance", [True, False])
def test_setup_managed_cloud(
    cloud_setup_failure, enable_head_node_fault_tolerance
) -> None:
    mock_region = "us-east-2"
    mock_cloud_name = "mock_cloud_name"
    mock_cloud_id = "mock_cloud_id"
    mock_anyscale_iam_role_name = "mock_anyscale_iam_role_name"
    mock_ray_iam_role_name = f"{mock_cloud_id}-cluster_node_role"
    mock_cfn_stack = "mock_cfn_stack"
    mock_api_client = Mock()
    mock_prepare_for_managed_cloud_setup = Mock(
        return_value=(mock_anyscale_iam_role_name, mock_cloud_id)
    )
    mock_run_cloudformation = Mock(return_value=mock_cfn_stack)
    mock_update_cloud_with_resources = Mock()

    cluster_management_stack_version = ClusterManagementStackVersions.V2

    if cloud_setup_failure:
        mock_update_cloud_with_resources.side_effect = Exception("ERROR")

    with patch.multiple(
        "anyscale.controllers.cloud_controller.CloudController",
        prepare_for_managed_cloud_setup=mock_prepare_for_managed_cloud_setup,
        run_cloudformation=mock_run_cloudformation,
        update_cloud_with_resources=mock_update_cloud_with_resources,
    ):
        cloud_controller = CloudController()
        cloud_controller.api_client = mock_api_client
        if cloud_setup_failure:
            with pytest.raises(ClickException):
                cloud_controller.setup_managed_cloud(
                    provider="aws",
                    region=mock_region,
                    name=mock_cloud_name,
                    functional_verify=None,
                    cluster_management_stack_version=cluster_management_stack_version,
                    enable_head_node_fault_tolerance=enable_head_node_fault_tolerance,
                )
        else:
            cloud_controller.setup_managed_cloud(
                provider="aws",
                region=mock_region,
                name=mock_cloud_name,
                functional_verify=None,
                cluster_management_stack_version=cluster_management_stack_version,
                enable_head_node_fault_tolerance=enable_head_node_fault_tolerance,
            )

    mock_prepare_for_managed_cloud_setup.assert_called_with(
        mock_region, mock_cloud_name, cluster_management_stack_version
    )
    mock_run_cloudformation.assert_called_with(
        mock_region,
        mock_cloud_id,
        mock_anyscale_iam_role_name,
        mock_ray_iam_role_name,
        enable_head_node_fault_tolerance,
        _use_strict_iam_permissions=False,
    )
    mock_update_cloud_with_resources.assert_called_with(
        mock_cfn_stack, mock_cloud_id, enable_head_node_fault_tolerance
    )

    if cloud_setup_failure:
        mock_api_client.delete_cloud_api_v2_clouds_cloud_id_delete.assert_called_with(
            cloud_id=mock_cloud_id
        )


@pytest.mark.parametrize(
    ("cloud_setup_failure", "deployment_manager_failure"),
    [
        pytest.param(False, False, id="success",),
        pytest.param(True, True, id="failure-keep-deployment",),
        pytest.param(True, False, id="failure-clean-up-deployment",),
    ],
)
def test_setup_managed_cloud_gcp(
    cloud_setup_failure, deployment_manager_failure
) -> None:
    mock_region = "us-west1"
    mock_cloud_name = "mock_cloud_name"
    mock_cloud_id = "mock_cloud_id"
    mock_deployment_name = mock_cloud_id.replace("_", "-").lower()
    mock_anyscale_aws_account = "123456"

    mock_factory = Mock()
    mock_gcp_utils = Mock(
        get_google_cloud_client_factory=Mock(return_value=mock_factory)
    )
    mock_setup_utils = Mock(
        delete_gcp_deployment=Mock(),
        delete_workload_identity_pool=Mock(),
        get_project_number=Mock(return_value="123456"),
        append_project_iam_policy=Mock(),
        enable_project_apis=Mock(),
    )

    mock_api_client = Mock(
        get_anyscale_aws_account_api_v2_clouds_anyscale_aws_account_get=Mock(
            return_value=Mock(
                result=Mock(anyscale_aws_account=mock_anyscale_aws_account)
            )
        )
    )

    mock_anyscale_service_account = "anyscale-access-mock@abc.com"
    mock_project_id = "mock-project"
    mock_project_number = "112233445566"
    mock_pool_id = "mock-pool"
    mock_pool_name = f"projects/{mock_project_number}/locations/global/workloadIdentityPools/{mock_pool_id}"
    mock_prepare_for_managed_cloud_setup_gcp = Mock(
        return_value=(mock_anyscale_service_account, mock_pool_name, mock_cloud_id)
    )
    mock_run_deployment_manager = Mock()
    mock_update_cloud_with_resources_gcp = Mock()
    mock_create_workload_identity_federation_provider = Mock()
    mock_org_id = "org_abc"

    cluster_management_stack_version = ClusterManagementStackVersions.V2

    if cloud_setup_failure:
        if deployment_manager_failure:
            mock_run_deployment_manager.side_effect = ClickException("ERROR")
        else:
            mock_update_cloud_with_resources_gcp.side_effect = Exception("ERROR")

    with patch.multiple(
        "anyscale.controllers.cloud_controller.CloudController",
        prepare_for_managed_cloud_setup_gcp=mock_prepare_for_managed_cloud_setup_gcp,
        run_deployment_manager=mock_run_deployment_manager,
        update_cloud_with_resources_gcp=mock_update_cloud_with_resources_gcp,
        create_workload_identity_federation_provider=mock_create_workload_identity_federation_provider,
    ), patch.multiple(
        "anyscale.controllers.cloud_controller",
        get_organization_id=Mock(return_value=mock_org_id),
        try_import_gcp_utils=Mock(return_value=mock_gcp_utils),
        try_import_gcp_managed_setup_utils=Mock(return_value=mock_setup_utils),
    ):
        cloud_controller = CloudController()
        cloud_controller.api_client = mock_api_client
        if cloud_setup_failure:
            with pytest.raises(ClickException) as e:
                cloud_controller.setup_managed_cloud(
                    provider="gcp",
                    region=mock_region,
                    name=mock_cloud_name,
                    functional_verify=None,
                    cluster_management_stack_version=cluster_management_stack_version,
                    enable_head_node_fault_tolerance=False,
                    project_id=mock_project_id,
                )
            e.match("Cloud setup failed")
            mock_api_client.delete_cloud_api_v2_clouds_cloud_id_delete.assert_called_with(
                cloud_id=mock_cloud_id
            )
            if deployment_manager_failure:
                mock_setup_utils.delete_gcp_deployment.assert_not_called()
            else:
                mock_setup_utils.delete_gcp_deployment.assert_called_once_with(
                    mock_factory, mock_project_id, mock_deployment_name
                )
            mock_setup_utils.delete_workload_identity_pool.assert_called_once_with(
                mock_factory, mock_pool_name, cloud_controller.log
            )

        else:
            cloud_controller.setup_managed_cloud(
                provider="gcp",
                region=mock_region,
                name=mock_cloud_name,
                functional_verify=None,
                cluster_management_stack_version=cluster_management_stack_version,
                enable_head_node_fault_tolerance=False,
                project_id=mock_project_id,
            )

    mock_prepare_for_managed_cloud_setup_gcp.assert_called_with(
        mock_project_id,
        mock_region,
        mock_cloud_name,
        mock_factory,
        cluster_management_stack_version,
    )
    mock_create_workload_identity_federation_provider.assert_called_once_with(
        mock_factory, mock_project_id, mock_pool_id, mock_anyscale_service_account
    )
    mock_run_deployment_manager.assert_called_with(
        mock_factory,
        mock_deployment_name,
        mock_cloud_id,
        mock_project_id,
        mock_region,
        mock_anyscale_service_account,
        mock_pool_name,
        mock_anyscale_aws_account,
        mock_org_id,
        False,
    )
    if deployment_manager_failure:
        mock_update_cloud_with_resources_gcp.assert_not_called()
    else:
        mock_update_cloud_with_resources_gcp.assert_called_with(
            mock_factory,
            mock_deployment_name,
            mock_cloud_id,
            mock_project_id,
            mock_anyscale_service_account,
        )


@pytest.mark.parametrize("provider", ["AWS", "GCP"])
@pytest.mark.parametrize("no_resource_record", [True, False])
def test_delete_cloud(provider: str, no_resource_record: bool):
    mock_cloud_id = "mock_cloud_id"
    mock_cloud_name = "mock_cloud_name"
    with patch.multiple(
        "anyscale.controllers.cloud_controller",
        get_cloud_id_and_name=Mock(return_value=(mock_cloud_id, mock_cloud_name)),
        get_cloud_resource_by_cloud_id=Mock(
            return_value=None if no_resource_record else Mock()
        ),
        confirm=Mock(return_value=True),
        try_delete_customer_drifts_policy=Mock(),
    ):
        cloud_controller = CloudController()
        mock_log_spinner = MagicMock()
        mock_log_spinner.return_value.__enter__.return_value = Mock()
        cloud_controller.log = Mock(spinner=mock_log_spinner)
        mock_cloud = Mock(
            result=Mock(provider=provider, is_bring_your_own_resource=False,)
        )
        cloud_controller.api_client.get_cloud_api_v2_clouds_cloud_id_get = Mock(
            return_value=mock_cloud
        )
        cloud_controller.api_client.update_cloud_with_cloud_resource_api_v2_clouds_with_cloud_resource_router_cloud_id_put = Mock(
            return_value=mock_cloud
        )
        cloud_controller.api_client.update_cloud_with_cloud_resource_api_v2_clouds_with_cloud_resource_gcp_router_cloud_id_put = Mock(
            return_value=mock_cloud
        )

        cloud_controller.api_client.delete_cloud_api_v2_clouds_cloud_id_delete = Mock()
        cloud_controller.delete_aws_managed_cloud = Mock()  # type: ignore[assignment]
        cloud_controller.delete_tagged_managed_resources = Mock()  # type: ignore[assignment]
        cloud_controller.delete_tls_certs = Mock()  # type: ignore[assignment]
        cloud_controller.delete_gcp_managed_cloud = Mock()  # type: ignore[assignment]
        mock_confirm = Mock(return_value=True)

        with patch(cloud_controller.__module__ + ".confirm", new=mock_confirm):
            cloud_controller.delete_cloud(
                cloud_name=mock_cloud_name,
                cloud_id=mock_cloud_id,
                skip_confirmation=False,
            )

        cloud_controller.api_client.delete_cloud_api_v2_clouds_cloud_id_delete.assert_called_with(
            cloud_id=mock_cloud_id
        )

        if no_resource_record:
            mock_confirm.assert_not_called()
            return

        mock_confirm.assert_called_once()

        if provider == "AWS":
            cloud_controller.delete_aws_managed_cloud.assert_called_with(
                cloud=mock_cloud.result
            )
            cloud_controller.delete_tagged_managed_resources.assert_called_with(
                cloud=mock_cloud.result
            )
            cloud_controller.delete_tls_certs.assert_called_with(
                cloud=mock_cloud.result
            )

            cloud_controller.delete_aws_managed_cloud.assert_called_with(
                cloud=mock_cloud.result
            )
            cloud_controller.api_client.update_cloud_with_cloud_resource_api_v2_clouds_with_cloud_resource_router_cloud_id_put.assert_called_with(
                cloud_id=mock_cloud_id,
                update_cloud_with_cloud_resource=UpdateCloudWithCloudResource(
                    state=CloudState.DELETING
                ),
            )
        elif provider == "GCP":
            cloud_controller.delete_gcp_managed_cloud.assert_called_with(
                cloud=mock_cloud.result
            )
            cloud_controller.api_client.update_cloud_with_cloud_resource_api_v2_clouds_with_cloud_resource_gcp_router_cloud_id_put.assert_called_with(
                cloud_id=mock_cloud_id,
                update_cloud_with_cloud_resource_gcp=UpdateCloudWithCloudResourceGCP(
                    state=CloudState.DELETING
                ),
            )


@pytest.mark.parametrize("exception_delete_managed_resources", [True, False])
@pytest.mark.parametrize("exception_delete_tls_certs", [True, False])
@mock_cloudformation
def test_fail_delete_service_resources(
    exception_delete_managed_resources: bool, exception_delete_tls_certs: bool
):
    """
    If either delete_tagged_managed_resources, or delete_tls_certs throws an exception,
    make sure that delete_aws_managed_cloud is not called
    """

    cloud_controller = CloudController()
    mock_log_spinner = MagicMock()
    mock_log_spinner.return_value.__enter__.return_value = Mock()
    cloud_controller.log = Mock(spinner=mock_log_spinner)

    cloud_controller.delete_tagged_managed_resources = Mock()  # type: ignore[assignment]
    cloud_controller.delete_tls_certs = Mock()  # type: ignore[assignment]
    cloud_controller.delete_aws_managed_cloud = Mock()  # type: ignore[assignment]

    with patch.multiple(
        "anyscale.controllers.cloud_controller",
        try_delete_customer_drifts_policy=Mock(),
    ):
        if exception_delete_managed_resources:
            cloud_controller.delete_tagged_managed_resources.side_effect = ClickException(
                "Mock Error"
            )

        if exception_delete_tls_certs:
            cloud_controller.delete_tls_certs.side_effect = ClickException("Mock Error")

        if exception_delete_managed_resources or exception_delete_tls_certs:
            with pytest.raises(ClickException):
                cloud_controller.delete_all_aws_resources(Mock(), Mock())

            cloud_controller.delete_aws_managed_cloud.assert_not_called()

        else:
            cloud_controller.delete_all_aws_resources(Mock(), Mock())
            cloud_controller.delete_aws_managed_cloud.assert_called_once()


@pytest.mark.parametrize("pre_deleted", [True, False])
@mock_cloudformation
def test_delete_aws_managed_cloud(pre_deleted: bool):
    cfn = boto3.client("cloudformation", region_name="us-west-2")
    stack_response = cfn.create_stack(
        StackName="stack_name", TemplateBody="{Resources: {}}"
    )
    stack_id = stack_response["StackId"]
    if pre_deleted:
        cfn.delete_stack(StackName=stack_id)

    cloud_mock = Mock(
        id="mock_cloud_id",
        region="us-west-2",
        cloud_resource=Mock(aws_cloudformation_stack_id=stack_id,),
    )
    cloud_controller = CloudController()
    mock_log_spinner = MagicMock()
    mock_log_spinner.return_value.__enter__.return_value = Mock()
    cloud_controller.log = Mock(spinner=mock_log_spinner)

    with patch.object(
        cloud_controller,
        "delete_aws_cloudformation_stack",
        return_value=cloud_controller.delete_aws_cloudformation_stack,
    ) as mock_delete_aws_cloudformation_stack:

        assert cloud_controller.delete_aws_managed_cloud(cloud=cloud_mock)

        mock_delete_aws_cloudformation_stack.assert_called_once_with(
            cfn_stack_arn=stack_id, cloud=cloud_mock
        )

        assert mock_delete_aws_cloudformation_stack.return_value


@pytest.mark.parametrize("pre_deleted", [True, False])
@mock_acm
def test_delete_tls_certs(pre_deleted: bool):
    mock_cloud_id = "mock_cloud_id"

    acm = boto3.client("acm", region_name="us-west-2")

    aws_tags: List[cf_types.TagTypeDef] = [
        {"Key": "anyscale-cloud-id", "Value": mock_cloud_id}
    ]
    domain = "mockdomain.com"
    acm_response = acm.request_certificate(
        DomainName=domain, ValidationMethod="DNS", Tags=aws_tags,
    )

    certificates = acm.list_certificates()
    assert certificates["CertificateSummaryList"]

    certificate_arn = acm_response["CertificateArn"]
    if pre_deleted:
        acm.delete_certificate(CertificateArn=certificate_arn)

    cloud_mock = Mock(id=mock_cloud_id, region="us-west-2", cloud_resource=Mock(),)
    cloud_controller = CloudController()
    mock_log_spinner = MagicMock()
    mock_log_spinner.return_value.__enter__.return_value = Mock()
    cloud_controller.log = Mock(spinner=mock_log_spinner)

    assert cloud_controller.delete_tls_certs(cloud=cloud_mock)

    # Check that the TLS cert was deleted
    certificates = acm.list_certificates()
    assert not certificates["CertificateSummaryList"]


@pytest.mark.parametrize("pre_deleted", [True, False])
@mock_cloudformation
def test_delete_tagged_managed_resources(pre_deleted: bool):
    mock_cloud_id = "mock_cloud_id"

    cfn = boto3.client("cloudformation", region_name="us-west-2")
    aws_tags: List[cf_types.TagTypeDef] = [
        {"Key": "anyscale-cloud-id", "Value": mock_cloud_id}
    ]

    stack_response = cfn.create_stack(
        StackName="stack_name", TemplateBody="{Resources: {}}", Tags=aws_tags,
    )
    stack_id = stack_response["StackId"]
    if pre_deleted:
        cfn.delete_stack(StackName=stack_id)

    cloud_mock = Mock(
        id=mock_cloud_id,
        region="us-west-2",
        cloud_resource=Mock(aws_cloudformation_stack_id=stack_id,),
    )
    cloud_controller = CloudController()
    mock_log_spinner = MagicMock()
    mock_log_spinner.return_value.__enter__.return_value = Mock()
    cloud_controller.log = Mock(spinner=mock_log_spinner)

    with patch.object(
        cloud_controller,
        "delete_aws_cloudformation_stack",
        return_value=cloud_controller.delete_aws_cloudformation_stack,
    ) as mock_delete_aws_cloudformation_stack:

        assert cloud_controller.delete_tagged_managed_resources(cloud=cloud_mock)

        mock_delete_aws_cloudformation_stack.assert_called_once_with(
            cfn_stack_arn=stack_id, cloud=cloud_mock
        )

        assert mock_delete_aws_cloudformation_stack.return_value


@pytest.mark.parametrize("valid_stack_id", [True, False])
@mock_cloudformation
def test_delete_aws_cloudformation_stack(valid_stack_id: bool):
    mock_cloud_id = "mock_cloud_id"

    cfn = boto3.client("cloudformation", region_name="us-west-2")

    stack_response = cfn.create_stack(
        StackName="stack_name", TemplateBody="{Resources: {}}",
    )
    stack_id = stack_response["StackId"]
    cloud_mock = Mock(
        id=mock_cloud_id,
        region="us-west-2",
        cloud_resource=Mock(aws_cloudformation_stack_id=stack_id,),
    )
    cloud_controller = CloudController()
    mock_log_spinner = MagicMock()
    mock_log_spinner.return_value.__enter__.return_value = Mock()
    cloud_controller.log = Mock(spinner=mock_log_spinner)

    if valid_stack_id:
        assert cloud_controller.delete_aws_cloudformation_stack(
            cfn_stack_arn=stack_id, cloud=cloud_mock
        )
    else:
        with pytest.raises(
            ClickException, match=r"Failed to fetch the cloudformation stack",
        ):
            cloud_controller.delete_aws_cloudformation_stack(
                cfn_stack_arn="mock_id", cloud=cloud_mock
            )


@mock_cloudformation
def test_delete_aws_managed_cloud_invalid_cloudformation_stack():
    cloud_mock = Mock(
        id="mock_cloud_id",
        region="us-west-2",
        cloud_resource=Mock(aws_cloudformation_stack_id="invalid_id"),
    )
    cloud_controller = CloudController()
    mock_log_spinner = MagicMock()
    mock_log_spinner.return_value.__enter__.return_value = Mock()
    cloud_controller.log = Mock(spinner=mock_log_spinner)

    with pytest.raises(ClickException) as e:
        cloud_controller.delete_aws_managed_cloud(cloud=cloud_mock,)

    assert "Failed to fetch the cloudformation stack" in e.value.message


@pytest.mark.parametrize("projects_match", [True, False])
def test_gcp_verify_credentials_project(capsys, projects_match: bool):
    cloud_controller = CloudController()
    mock_region = "mock_region"
    mock_project_id = "mock_project_id"

    credentials_project = mock_project_id if projects_match else "other_gcp_project"
    mock_verify_lib = Mock()
    mock_verify_lib.verify_cloud_storage = Mock()
    mock_verify_lib.verify_filestore = Mock()
    mock_verify_lib.verify_firewall_policy = Mock()
    mock_verify_lib.verify_gcp_access_service_account = Mock()
    mock_verify_lib.verify_gcp_dataplane_service_account = Mock()
    mock_verify_lib.verify_gcp_networking = Mock()
    mock_verify_lib.verify_gcp_project = Mock()

    with patch.multiple(
        "anyscale.controllers.cloud_controller",
        try_import_gcp_verify_lib=Mock(return_value=mock_verify_lib),
    ), patch.multiple(
        "anyscale.utils.gcp_utils",
        get_application_default_credentials=Mock(
            return_value=(AnonymousCredentials(), credentials_project)
        ),
        GoogleCloudClientFactory=Mock(),
    ) as all_mocks:
        assert cloud_controller.verify_gcp_cloud_resources(
            cloud_resource=Mock(),
            project_id=mock_project_id,
            region=mock_region,
            cloud_id="cld_abc",
            yes=False,
        )
        all(mock_fn.assert_called_once() for mock_fn in all_mocks.values())

    _, err = capsys.readouterr()
    assert ("Default credentials are for" in err) != projects_match


@pytest.mark.parametrize("empty_deployment_name", [True, False])
def test_delete_gcp_managed_cloud(empty_deployment_name: bool):
    mock_project = "mock-project"
    mock_firewall = "mock-firewall"
    mock_deployment = None if empty_deployment_name else "mock-deployment"
    mock_credentials = json.dumps({"project_id": "mock-project"})
    mock_resources = Mock(
        gcp_deployment_manager_id=mock_deployment,
        gcp_firewall_policy_ids=[mock_firewall],
        gcp_cloud_storage_bucket_id="mock-bucket",
    )

    cloud_mock = Mock(
        id="mock_cloud_id",
        region="us-west1",
        credentials=mock_credentials,
        cloud_resource=mock_resources,
    )

    if empty_deployment_name:
        with pytest.raises(ClickException) as e:
            CloudController().delete_gcp_managed_cloud(cloud_mock)
        e.match(" does not have a deployment in GCP deployment manager.")
    else:
        mock_factory = Mock()
        gcp_utils_mock = Mock(
            get_google_cloud_client_factory=Mock(return_value=mock_factory)
        )
        setup_utils_mock = Mock(
            remove_firewall_policy_associations=Mock(),
            update_deployment_with_bucket_only=Mock(),
        )
        with patch.multiple(
            "anyscale.controllers.cloud_controller",
            try_import_gcp_managed_setup_utils=Mock(return_value=setup_utils_mock),
            try_import_gcp_utils=Mock(return_value=gcp_utils_mock),
        ):
            cloud_controller = CloudController()
            assert cloud_controller.delete_gcp_managed_cloud(cloud_mock) is True
            gcp_utils_mock.get_google_cloud_client_factory.assert_called_once_with(
                cloud_controller.log, mock_project
            )
            setup_utils_mock.remove_firewall_policy_associations.assert_called_once_with(
                mock_factory, mock_project, mock_firewall
            )
            setup_utils_mock.update_deployment_with_bucket_only.assert_called_once_with(
                mock_factory, mock_project, mock_deployment
            )


@pytest.mark.parametrize("enable_head_node_fault_tolerance", [True, False])
@mock_cloudformation
def test_update_cloud_with_resources_aws(enable_head_node_fault_tolerance: bool):
    api_client_mock = Mock()
    api_client_mock.update_cloud_with_cloud_resource_api_v2_clouds_with_cloud_resource_router_cloud_id_put = (
        Mock()
    )

    region = "us-west-2"
    boto3.client("cloudformation", region_name=region)
    mock_cloud_id = "mock_cloud_id"
    mock_stack_id = "mock-cloud-id"
    mock_memorydb_config = (
        '{"arn": "mock-arn", "ClusterEndpointAddress": "mock-endpoint"}'
    )
    mock_cfn_stack = {
        "Outputs": [
            {
                "OutputKey": "SubnetsWithAvailabilityZones",
                "OutputValue": '[{"subnet_id": "mock_subnet_id", "availability_zone": "mock_availability_zone"}]',
            },
            {"OutputKey": "VPC", "OutputValue": "mock-vpc"},
            {"OutputKey": "AnyscaleSecurityGroup", "OutputValue": "mock-sg"},
            {"OutputKey": "S3Bucket", "OutputValue": "mock-s3"},
            {"OutputKey": "EFS", "OutputValue": "mock-efs"},
            {
                "OutputKey": "EFSMountTargetIP",
                "OutputValue": "mock-efs-mount-target-ip",
            },
            {"OutputKey": "AnyscaleIAMRole", "OutputValue": "mock-iam-role"},
            {"OutputKey": "NodeIamRole", "OutputValue": "mock-node-iam-role"},
            {"OutputKey": "MemoryDB", "OutputValue": mock_memorydb_config},
        ],
        "StackId": mock_stack_id,
    }

    cloud_controller = CloudController()
    cloud_controller.api_client = api_client_mock

    cloud_controller.update_cloud_with_resources(
        mock_cfn_stack, mock_cloud_id, enable_head_node_fault_tolerance
    )

    api_client_mock.update_cloud_with_cloud_resource_api_v2_clouds_with_cloud_resource_router_cloud_id_put.assert_called_once_with(
        cloud_id=mock_cloud_id,
        update_cloud_with_cloud_resource=UpdateCloudWithCloudResource(
            cloud_resource_to_update=CreateCloudResource(
                aws_cloudformation_stack_id="mock-cloud-id",
                aws_vpc_id="mock-vpc",
                aws_subnet_ids_with_availability_zones=[
                    SubnetIdWithAvailabilityZoneAWS(
                        subnet_id="mock_subnet_id",
                        availability_zone="mock_availability_zone",
                    )
                ],
                aws_security_groups=["mock-sg"],
                aws_s3_id="mock-s3",
                aws_efs_id="mock-efs",
                aws_efs_mount_target_ip="mock-efs-mount-target-ip",
                aws_iam_role_arns=["mock-iam-role", "mock-node-iam-role"],
                memorydb_cluster_config=AWSMemoryDBClusterConfig(
                    id="mock-arn", endpoint="rediss://mock-endpoint:6379"
                )
                if enable_head_node_fault_tolerance
                else None,
            )
        ),
    )


@pytest.mark.parametrize("configure_firewall_fail", [True, False])
@pytest.mark.parametrize("update_resource_fail", [True, False])
def test_update_cloud_with_resources_gcp(
    configure_firewall_fail: bool, update_resource_fail: bool
):
    mock_resources = {}
    mock_resources["compute.v1.network"] = "mock-vpc"
    mock_resources["compute.v1.subnetwork"] = "mock-subnet"
    mock_resources["iam.v1.serviceAccount"] = "mock-cluster"
    mock_resources["gcp-types/compute-v1:networkFirewallPolicies"] = "mock-firewall"
    mock_resources["storage.v1.bucket"] = "mock-bucket"
    mock_resources["filestore_location"] = "mock-zone"
    mock_resources["filestore_instance"] = "mock-filestore"

    setup_utils_mock = Mock()
    setup_utils_mock.get_deployment_resources = Mock(return_value=mock_resources)
    setup_utils_mock.configure_firewall_policy = (
        Mock(side_effect=ClickException("error")) if configure_firewall_fail else Mock()
    )
    setup_utils_mock.remove_firewall_policy_associations = Mock()
    try_import_gcp_managed_setup_utils_mock = Mock(return_value=setup_utils_mock)

    gcp_utils_mock = Mock()
    gcp_utils_mock.get_gcp_filestore_config = Mock()
    try_import_gcp_utils_mock = Mock(return_value=setup_utils_mock)

    mock_anyscale_access_service_account = "abc@abc.com"
    mock_cloud_id = "cld_abc"
    mock_deployment_name = "cld-abc"
    mock_project_id = "mock-project"
    mock_factory = Mock()

    api_client_mock = Mock()
    api_client_mock.update_cloud_with_cloud_resource_api_v2_clouds_with_cloud_resource_gcp_router_cloud_id_put = (
        Mock(side_effect=ClickException("error")) if update_resource_fail else Mock()
    )
    cloud_controller = CloudController()
    cloud_controller.api_client = api_client_mock

    if configure_firewall_fail or update_resource_fail:
        with pytest.raises(ClickException) as e, patch.multiple(
            "anyscale.controllers.cloud_controller",
            try_import_gcp_managed_setup_utils=try_import_gcp_managed_setup_utils_mock,
            try_import_gcp_utils=try_import_gcp_utils_mock,
        ):
            cloud_controller.update_cloud_with_resources_gcp(
                mock_factory,
                mock_deployment_name,
                mock_cloud_id,
                mock_project_id,
                mock_anyscale_access_service_account,
            )
        e.match("Error occurred when updating resources")
    else:
        # happy path
        with patch.multiple(
            "anyscale.controllers.cloud_controller",
            try_import_gcp_managed_setup_utils=try_import_gcp_managed_setup_utils_mock,
            try_import_gcp_utils=try_import_gcp_utils_mock,
        ):
            assert (
                cloud_controller.update_cloud_with_resources_gcp(
                    mock_factory,
                    mock_deployment_name,
                    mock_cloud_id,
                    mock_project_id,
                    mock_anyscale_access_service_account,
                )
                is None
            )


@pytest.mark.parametrize(
    ("functions_to_verify", "valid", "expected_returned_result"),
    [
        (None, True, []),
        ("workspace", True, [CloudFunctionalVerificationType.WORKSPACE],),
        (
            "WORKSPACE,servIce",
            True,
            [
                CloudFunctionalVerificationType.WORKSPACE,
                CloudFunctionalVerificationType.SERVICE,
            ],
        ),
        ("invalid", False, [],),
        ("service,invalid", False, [],),
    ],
)
def test_validate_functional_verification_args(
    functions_to_verify: Optional[str],
    valid: bool,
    expected_returned_result: List[str],
):
    # TODO (congding): add test cases for "service"
    if valid:
        assert set(
            CloudController()._validate_functional_verification_args(
                functions_to_verify
            )
        ) == set(expected_returned_result)
    else:
        with pytest.raises(ClickException) as e:
            CloudController()._validate_functional_verification_args(
                functions_to_verify
            )
        e.match("Unsupported function")


### Test edit cloud ###
@pytest.mark.parametrize(
    ("get_mount_target_ip_succeed", "static_verify_succeed", "api_call_succeed",),
    [
        pytest.param(True, True, True),
        pytest.param(False, True, True),
        pytest.param(True, False, True),
        pytest.param(True, True, False),
    ],
)
def test_edit_aws_cloud(
    get_mount_target_ip_succeed: bool,
    static_verify_succeed: bool,
    api_call_succeed: bool,
):
    mock_cloud = Mock()
    mock_cloud.region = "us-west-2"
    mock_cloud.is_bring_your_own_resource = False
    mock_cloud.is_private_cloud = False
    mock_cloud_resource = CreateCloudResource(
        aws_s3_id="old_aws_s3_id",
        aws_efs_id="old_aws_efs_id",
        aws_efs_mount_target_ip="old_aws_efs_mount_target_ip",
    )
    mock_get_aws_efs_mount_target_ip = (
        Mock(return_value="new_aws_efs_mount_target_ip")
        if get_mount_target_ip_succeed
        else Mock(side_effect=ClickException("failed to get mount target ip"))
    )
    mock_verify_aws_cloud_resources = Mock(return_value=static_verify_succeed)
    mock_edit_cloud_resource_api = (
        Mock()
        if api_call_succeed
        else Mock(side_effect=ClickException("failed to edit cloud"))
    )
    new_memorydb_cluster_config = AWSMemoryDBClusterConfig(
        id="new_memorydb_cluster_config_id", endpoint="new-mock-endpoint:6379"
    )
    mock_get_memorydb_cluster_config = Mock(return_value=new_memorydb_cluster_config)

    with patch.multiple(
        "anyscale.controllers.cloud_controller",
        _get_aws_efs_mount_target_ip=mock_get_aws_efs_mount_target_ip,
        _get_memorydb_cluster_config=mock_get_memorydb_cluster_config,
    ), patch(
        "anyscale.controllers.cloud_controller.CloudController.verify_aws_cloud_resources",
        mock_verify_aws_cloud_resources,
    ):
        cloud_controller = CloudController()
        cloud_controller.cloud_event_producer = Mock()
        cloud_controller.log = Mock()
        cloud_controller.api_client.edit_cloud_resource_api_v2_clouds_with_cloud_resource_router_cloud_id_patch = (
            mock_edit_cloud_resource_api
        )
        # happy path.
        if all([get_mount_target_ip_succeed, static_verify_succeed, api_call_succeed,]):
            # Edit aws_s3_id succeed.
            cloud_controller._edit_aws_cloud(
                cloud_name="mock_cloud_name",
                cloud_id="mock_cloud_id",
                cloud=mock_cloud,
                cloud_resource=mock_cloud_resource,
                aws_s3_id="new_aws_s3_id",
                aws_efs_id="",
                aws_efs_mount_target_ip="",
                memorydb_cluster_id="",
                yes=True,
            )
            mock_edit_cloud_resource_api.assert_called_with(
                cloud_id="mock_cloud_id",
                editable_cloud_resource=EditableCloudResource(
                    aws_s3_id="new_aws_s3_id",
                    aws_efs_id="",
                    aws_efs_mount_target_ip="",
                    memorydb_cluster_config=None,
                ),
            )
            # Edit aws_efs_id succeed. (should get aws_efs_mount_target_ip for the aws_efs_id).
            cloud_controller._edit_aws_cloud(
                cloud_name="mock_cloud_name",
                cloud_id="mock_cloud_id",
                cloud=mock_cloud,
                cloud_resource=mock_cloud_resource,
                aws_s3_id="",
                aws_efs_id="new_aws_efs_id",
                aws_efs_mount_target_ip="",
                memorydb_cluster_id="",
                yes=True,
            )
            mock_edit_cloud_resource_api.assert_called_with(
                cloud_id="mock_cloud_id",
                editable_cloud_resource=EditableCloudResource(
                    aws_s3_id="",
                    aws_efs_id="new_aws_efs_id",
                    aws_efs_mount_target_ip="new_aws_efs_mount_target_ip",
                    memorydb_cluster_config=None,
                ),
            )

            # Edit aws_efs_mount_target_ip succeed.
            cloud_controller._edit_aws_cloud(
                cloud_name="mock_cloud_name",
                cloud_id="mock_cloud_id",
                cloud=mock_cloud,
                cloud_resource=mock_cloud_resource,
                aws_s3_id="",
                aws_efs_id="",
                aws_efs_mount_target_ip="aws_efs_mount_target_ip_0",
                memorydb_cluster_id="",
                yes=True,
            )
            mock_edit_cloud_resource_api.assert_called_with(
                cloud_id="mock_cloud_id",
                editable_cloud_resource=EditableCloudResource(
                    aws_s3_id="",
                    aws_efs_id="",
                    aws_efs_mount_target_ip="aws_efs_mount_target_ip_0",
                    memorydb_cluster_config=None,
                ),
            )

            # Edit aws_efs_id and aws_efs_mount_target_ip succeed.
            cloud_controller._edit_aws_cloud(
                cloud_name="mock_cloud_name",
                cloud_id="mock_cloud_id",
                cloud=mock_cloud,
                cloud_resource=mock_cloud_resource,
                aws_s3_id="",
                aws_efs_id="new_aws_efs_id",
                aws_efs_mount_target_ip="aws_efs_mount_target_ip_0",
                memorydb_cluster_id="",
                yes=True,
            )
            mock_edit_cloud_resource_api.assert_called_with(
                cloud_id="mock_cloud_id",
                editable_cloud_resource=EditableCloudResource(
                    aws_s3_id="",
                    aws_efs_id="new_aws_efs_id",
                    aws_efs_mount_target_ip="aws_efs_mount_target_ip_0",
                    memorydb_cluster_config=None,
                ),
            )

            # Edit memorydb_cluster_id succeed.
            cloud_controller._edit_aws_cloud(
                cloud_name="mock_cloud_name",
                cloud_id="mock_cloud_id",
                cloud=mock_cloud,
                cloud_resource=mock_cloud_resource,
                aws_s3_id="",
                aws_efs_id="",
                aws_efs_mount_target_ip="",
                memorydb_cluster_id="new_memorydb_cluster_id",
                yes=True,
            )
            mock_edit_cloud_resource_api.assert_called_with(
                cloud_id="mock_cloud_id",
                editable_cloud_resource=EditableCloudResource(
                    aws_s3_id="",
                    aws_efs_id="",
                    aws_efs_mount_target_ip="",
                    memorydb_cluster_config=new_memorydb_cluster_config,
                ),
            )

            # Edit aws_s3_id, aws_efs_id and aws_efs_mount_target_ip, memorydb_cluster_id succeed.
            cloud_controller._edit_aws_cloud(
                cloud_name="mock_cloud_name",
                cloud_id="mock_cloud_id",
                cloud=mock_cloud,
                cloud_resource=mock_cloud_resource,
                aws_s3_id="new_aws_s3_id",
                aws_efs_id="new_aws_efs_id",
                aws_efs_mount_target_ip="aws_efs_mount_target_ip_0",
                memorydb_cluster_id="new_memorydb_cluster_id",
                yes=True,
            )

            mock_edit_cloud_resource_api.assert_called_with(
                cloud_id="mock_cloud_id",
                editable_cloud_resource=EditableCloudResource(
                    aws_s3_id="new_aws_s3_id",
                    aws_efs_id="new_aws_efs_id",
                    aws_efs_mount_target_ip="aws_efs_mount_target_ip_0",
                    memorydb_cluster_config=new_memorydb_cluster_config,
                ),
            )

            # Above input args are empty string "", this test input arg is None can also be handled.
            cloud_controller._edit_aws_cloud(
                cloud_name="mock_cloud_name",
                cloud_id="mock_cloud_id",
                cloud=mock_cloud,
                cloud_resource=mock_cloud_resource,
                aws_s3_id="new_aws_s3_id",
                aws_efs_id=None,
                aws_efs_mount_target_ip=None,
                memorydb_cluster_id=None,
                yes=True,
            )
            mock_edit_cloud_resource_api.assert_called_with(
                cloud_id="mock_cloud_id",
                editable_cloud_resource=EditableCloudResource(
                    aws_s3_id="new_aws_s3_id",
                    aws_efs_id=None,
                    aws_efs_mount_target_ip=None,
                    memorydb_cluster_config=None,
                ),
            )
        # error path.
        elif not get_mount_target_ip_succeed:
            with pytest.raises(ClickException) as e:
                cloud_controller._edit_aws_cloud(
                    cloud_name="mock_cloud_name",
                    cloud_id="mock_cloud_id",
                    cloud=mock_cloud,
                    cloud_resource=mock_cloud_resource,
                    aws_s3_id="",
                    aws_efs_id="new_aws_efs_id",
                    aws_efs_mount_target_ip="",
                    memorydb_cluster_id="",
                    yes=True,
                )
            e.match("Failed to get the mount target IP for new aws_efs_ip")
        elif not static_verify_succeed:
            with pytest.raises(ClickException) as e:
                cloud_controller._edit_aws_cloud(
                    cloud_name="mock_cloud_name",
                    cloud_id="mock_cloud_id",
                    cloud=mock_cloud,
                    cloud_resource=mock_cloud_resource,
                    aws_s3_id="",
                    aws_efs_id="",
                    aws_efs_mount_target_ip="",
                    memorydb_cluster_id="",
                    yes=True,
                )
            e.match("failed verification.")
        elif not api_call_succeed:
            with pytest.raises(ClickException) as e:
                cloud_controller._edit_aws_cloud(
                    cloud_name="mock_cloud_name",
                    cloud_id="mock_cloud_id",
                    cloud=mock_cloud,
                    cloud_resource=mock_cloud_resource,
                    aws_s3_id="",
                    aws_efs_id="",
                    aws_efs_mount_target_ip="",
                    memorydb_cluster_id="",
                    yes=True,
                )
            e.match("Edit cloud resource failed!")


def test_get_project_id():
    mock_cloud = Mock()
    cloud_controller = CloudController()
    cloud_controller.log = Mock()
    # No project id.
    with pytest.raises(ClickException) as e:
        cloud_controller._get_project_id(mock_cloud, "mock_cloud_name", "mock_cloud_id")
    e.match("Failed to get project id for cloud")

    # Has project id.
    mock_cloud.credentials = json.dumps({"project_id": "mock_project_id"})
    project_id = cloud_controller._get_project_id(
        mock_cloud, "mock_cloud_name", "mock_cloud_id"
    )
    assert project_id == "mock_project_id"


@pytest.mark.parametrize(
    ("static_verify_succeed", "api_call_succeed",),
    [pytest.param(True, True), pytest.param(False, True), pytest.param(True, False),],
)
def test_edit_gcp_cloud(
    static_verify_succeed: bool, api_call_succeed: bool,
):
    # Mock cloud and cloud_resource.
    mock_cloud = Mock()
    mock_cloud_resource = CreateCloudResourceGCP(
        gcp_filestore_config=GCPFileStoreConfig(
            instance_name="old_instance_name",
            root_dir="old_root_dir",
            mount_target_ip="old_mount_target_ip",
        ),
        gcp_cloud_storage_bucket_id="old_gcp_cloud_storage_bucket_id",
        gcp_vpc_id="mock_gcp_vpc_id",
        gcp_subnet_ids=["mock_gcp_subnet_id_0", "mock_gcp_subnet_id_1"],
        gcp_cluster_node_service_account_email="mock_gcp_cluster_node_service_account_email",
        gcp_anyscale_iam_service_account_email="mock_gcp_anyscale_iam_service_account_email",
        gcp_firewall_policy_ids=[
            "mock_gcp_firewall_policy_id_0",
            "mock_gcp_firewall_policy_id_1",
        ],
    )

    # Mock others.
    gcp_utils_mock = Mock()
    gcp_utils_mock.get_filestore_location_and_instance_id = Mock(
        return_value=("mock_old_filestore_location", "mock_old_filestore_instance_id")
    )
    gcp_utils_mock.get_google_cloud_client_factory = Mock()
    new_memorystore_instance_config = GCPMemorystoreInstanceConfig(
        name="new_memorystore_instance_name", endpoint="mock_endpoint:1234"
    )
    gcp_utils_mock.get_gcp_memorystore_config = Mock(
        return_value=new_memorystore_instance_config
    )
    mock_verify_gcp_cloud_resources = Mock(return_value=static_verify_succeed)
    mock_edit_cloud_resource_api = (
        Mock()
        if api_call_succeed
        else Mock(side_effect=ClickException("failed to edit cloud"))
    )

    # Test starts.
    with patch(
        "anyscale.controllers.cloud_controller.CloudController.verify_gcp_cloud_resources",
        mock_verify_gcp_cloud_resources,
    ), patch(
        "anyscale.controllers.cloud_controller.CloudController._get_project_id",
        Mock(return_value="mock_project_id"),
    ), patch(
        "anyscale.controllers.cloud_controller.CloudController._get_gcp_filestore_config",
        Mock(
            return_value=GCPFileStoreConfig(
                instance_name="mock_instance_name",
                root_dir="mock_root_dir",
                mount_target_ip="mock_mount_target_ip",
            )
        ),
    ), patch.multiple(
        "anyscale.controllers.cloud_controller",
        try_import_gcp_utils=Mock(return_value=gcp_utils_mock),
    ):
        cloud_controller = CloudController()
        cloud_controller.cloud_event_producer = Mock()
        cloud_controller.log = Mock()
        cloud_controller.api_client.edit_cloud_resource_api_v2_clouds_with_cloud_resource_gcp_router_cloud_id_patch = (
            mock_edit_cloud_resource_api
        )
        if all([static_verify_succeed, api_call_succeed,]):
            # Edit filestore_instance_id and filestore_location succeed.
            cloud_controller._edit_gcp_cloud(
                cloud_name="mock_cloud_name",
                cloud_id="mock_cloud_id",
                cloud=mock_cloud,
                cloud_resource=mock_cloud_resource,
                gcp_filestore_instance_id="new_filestore_instance_id",
                gcp_filestore_location="new_filestore_location",
                gcp_cloud_storage_bucket_name=None,
                memorystore_instance_name=None,
                yes=True,
            )
            mock_edit_cloud_resource_api.assert_called_with(
                cloud_id="mock_cloud_id",
                editable_cloud_resource_gcp=EditableCloudResourceGCP(
                    gcp_filestore_config=GCPFileStoreConfig(
                        # Should consistent with mock_get_gcp_filestore_config.
                        instance_name="mock_instance_name",
                        root_dir="mock_root_dir",
                        mount_target_ip="mock_mount_target_ip",
                    ),
                    gcp_cloud_storage_bucket_id=None,
                    memorystore_instance_config=None,
                ),
            )

            # Edit gcp_cloud_storage_bucket_id succeed.
            cloud_controller._edit_gcp_cloud(
                cloud_name="mock_cloud_name",
                cloud_id="mock_cloud_id",
                cloud=mock_cloud,
                cloud_resource=mock_cloud_resource,
                gcp_filestore_instance_id=None,
                gcp_filestore_location=None,
                gcp_cloud_storage_bucket_name="new_gcp_cloud_storage_bucket_name",
                memorystore_instance_name=None,
                yes=True,
            )
            mock_edit_cloud_resource_api.assert_called_with(
                cloud_id="mock_cloud_id",
                editable_cloud_resource_gcp=EditableCloudResourceGCP(
                    gcp_filestore_config=None,
                    gcp_cloud_storage_bucket_id="new_gcp_cloud_storage_bucket_name",
                    memorystore_instance_config=None,
                ),
            )

            # Edit memorystore_instance_config succeed.
            cloud_controller._edit_gcp_cloud(
                cloud_name="mock_cloud_name",
                cloud_id="mock_cloud_id",
                cloud=mock_cloud,
                cloud_resource=mock_cloud_resource,
                gcp_filestore_instance_id=None,
                gcp_filestore_location=None,
                gcp_cloud_storage_bucket_name="new_gcp_cloud_storage_bucket_name",
                memorystore_instance_name="new_memorystore_instance_name",
                yes=True,
            )
            mock_edit_cloud_resource_api.assert_called_with(
                cloud_id="mock_cloud_id",
                editable_cloud_resource_gcp=EditableCloudResourceGCP(
                    gcp_filestore_config=None,
                    gcp_cloud_storage_bucket_id="new_gcp_cloud_storage_bucket_name",
                    memorystore_instance_config=new_memorystore_instance_config,
                ),
            )

            # Edit filestore_instance_id, filestore_location, gcp_cloud_storage_bucket_id, memorystore_instance_name succeed.
            cloud_controller._edit_gcp_cloud(
                cloud_name="mock_cloud_name",
                cloud_id="mock_cloud_id",
                cloud=mock_cloud,
                cloud_resource=mock_cloud_resource,
                gcp_filestore_instance_id="new_filestore_instance_id",
                gcp_filestore_location="new_filestore_location",
                gcp_cloud_storage_bucket_name="new_gcp_cloud_storage_bucket_name",
                memorystore_instance_name="new_memorystore_instance_name",
                yes=True,
            )
            mock_edit_cloud_resource_api.assert_called_with(
                cloud_id="mock_cloud_id",
                editable_cloud_resource_gcp=EditableCloudResourceGCP(
                    gcp_filestore_config=GCPFileStoreConfig(
                        # Should consistent with mock_get_gcp_filestore_config.
                        instance_name="mock_instance_name",
                        root_dir="mock_root_dir",
                        mount_target_ip="mock_mount_target_ip",
                    ),
                    gcp_cloud_storage_bucket_id="new_gcp_cloud_storage_bucket_name",
                    memorystore_instance_config=new_memorystore_instance_config,
                ),
            )
        # error path
        if not static_verify_succeed:
            with pytest.raises(ClickException) as e:
                cloud_controller._edit_gcp_cloud(
                    cloud_name="mock_cloud_name",
                    cloud_id="mock_cloud_id",
                    cloud=mock_cloud,
                    cloud_resource=mock_cloud_resource,
                    gcp_filestore_instance_id="",
                    gcp_filestore_location="",
                    gcp_cloud_storage_bucket_name="new_gcp_cloud_storage_bucket_name",
                    memorystore_instance_name="",
                    yes=True,
                )
            e.match("failed verification")
        elif not api_call_succeed:
            with pytest.raises(ClickException) as e:
                cloud_controller._edit_gcp_cloud(
                    cloud_name="mock_cloud_name",
                    cloud_id="mock_cloud_id",
                    cloud=mock_cloud,
                    cloud_resource=mock_cloud_resource,
                    gcp_filestore_instance_id="",
                    gcp_filestore_location="",
                    gcp_cloud_storage_bucket_name="new_gcp_cloud_storage_bucket_name",
                    memorystore_instance_name="",
                    yes=True,
                )
            e.match("Edit cloud resource failed!")


@pytest.mark.parametrize(
    ("is_managed_cloud", "has_cloud_resource", "cloud_provider", "edit_succeed",),
    [
        pytest.param(False, True, "AWS", True),
        pytest.param(False, True, "GCP", True),
        pytest.param(False, False, "AWS", True),
        pytest.param(False, True, "AWS", False),
        pytest.param(True, True, "AWS", False),
    ],
)
def test_edit_cloud(
    has_cloud_resource: bool,
    cloud_provider: str,
    edit_succeed: bool,
    is_managed_cloud: bool,
):
    mock_cloud = Mock(
        result=Mock(
            provider=cloud_provider, is_bring_your_own_resource=not is_managed_cloud
        )
    )
    mock_get_cloud_resource_by_cloud_id = Mock(
        return_value=CreateCloudResource(
            aws_s3_id="old_aws_s3_id",
            aws_efs_id="old_aws_efs_id",
            aws_efs_mount_target_ip="old_aws_efs_mount_target_ip",
        )
        if has_cloud_resource
        else None
    )
    mock_edit_aws_cloud = (
        Mock()
        if edit_succeed
        else Mock(side_effect=ClickException("Edit cloud failed!"))
    )
    mock_edit_gcp_cloud = (
        Mock()
        if edit_succeed
        else Mock(side_effect=ClickException("Edit cloud failed!"))
    )
    with patch(
        "anyscale.controllers.cloud_controller.CloudController._validate_functional_verification_args",
        Mock(return_value=""),
    ), patch(
        "anyscale.controllers.cloud_controller.CloudController._edit_aws_cloud",
        mock_edit_aws_cloud,
    ), patch(
        "anyscale.controllers.cloud_controller.CloudController._edit_gcp_cloud",
        mock_edit_gcp_cloud,
    ), patch.multiple(
        "anyscale.controllers.cloud_controller",
        get_cloud_id_and_name=Mock(return_value=("mock_cloud_id", "mock_cloud_name")),
        get_cloud_resource_by_cloud_id=mock_get_cloud_resource_by_cloud_id,
    ):
        cloud_controller = CloudController()
        cloud_controller.cloud_event_producer = Mock()
        cloud_controller.log = Mock()
        cloud_controller.api_client.get_cloud_api_v2_clouds_cloud_id_get = Mock(
            return_value=mock_cloud
        )
        if all([has_cloud_resource, edit_succeed]):
            if cloud_provider == "AWS":
                # happy path.
                cloud_controller.edit_cloud(
                    cloud_id="mock_cloud_id",
                    cloud_name="",
                    aws_s3_id="mock_aws_s3_id",
                    aws_efs_id=None,
                    aws_efs_mount_target_ip=None,
                    memorydb_cluster_id=None,
                    gcp_filestore_instance_id=None,
                    gcp_filestore_location=None,
                    gcp_cloud_storage_bucket_name=None,
                    memorystore_instance_name=None,
                    functional_verify=None,
                    yes=True,
                )
                mock_edit_aws_cloud.assert_called_once()
                # error path: resource & provider mismatch exception.
                with pytest.raises(ClickException) as e:
                    cloud_controller.edit_cloud(
                        cloud_id="mock_cloud_id",
                        cloud_name="",
                        aws_s3_id=None,
                        aws_efs_id=None,
                        aws_efs_mount_target_ip=None,
                        memorydb_cluster_id=None,
                        gcp_filestore_instance_id=None,
                        gcp_filestore_location=None,
                        gcp_cloud_storage_bucket_name="mock_gcp_cloud_storage_bucket_name",
                        memorystore_instance_name=None,
                        functional_verify=None,
                        yes=True,
                    )
                e.match("Specified resource and provider mismatch")
            elif cloud_provider == "GCP":
                # happy path.
                cloud_controller.edit_cloud(
                    cloud_id="mock_cloud_id",
                    cloud_name="",
                    aws_s3_id=None,
                    aws_efs_id=None,
                    aws_efs_mount_target_ip=None,
                    memorydb_cluster_id=None,
                    gcp_filestore_instance_id=None,
                    gcp_filestore_location=None,
                    gcp_cloud_storage_bucket_name="mock_gcp_cloud_storage_bucket_name",
                    memorystore_instance_name=None,
                    functional_verify=None,
                    yes=True,
                )
                mock_edit_gcp_cloud.assert_called_once()
                with pytest.raises(ClickException) as e:
                    cloud_controller.edit_cloud(
                        cloud_id="mock_cloud_id",
                        cloud_name="",
                        aws_s3_id="mock_aws_s3_id",
                        aws_efs_id=None,
                        aws_efs_mount_target_ip=None,
                        memorydb_cluster_id=None,
                        gcp_filestore_instance_id=None,
                        gcp_filestore_location=None,
                        gcp_cloud_storage_bucket_name=None,
                        memorystore_instance_name=None,
                        functional_verify=None,
                        yes=True,
                    )
                e.match("Specified resource and provider mismatch")
        # error path.
        elif not has_cloud_resource:
            with pytest.raises(ClickException) as e:
                cloud_controller.edit_cloud(
                    cloud_id="mock_cloud_id",
                    cloud_name="",
                    aws_s3_id=None,
                    aws_efs_id=None,
                    aws_efs_mount_target_ip=None,
                    memorydb_cluster_id=None,
                    gcp_filestore_instance_id=None,
                    gcp_filestore_location=None,
                    gcp_cloud_storage_bucket_name=None,
                    memorystore_instance_name=None,
                    functional_verify=None,
                    yes=True,
                )
            e.match("does not contain resource records")
        elif not edit_succeed:
            with pytest.raises(ClickException) as e:
                cloud_controller.edit_cloud(
                    cloud_id="mock_cloud_id",
                    cloud_name="",
                    aws_s3_id=None,
                    aws_efs_id=None,
                    aws_efs_mount_target_ip=None,
                    memorydb_cluster_id=None,
                    gcp_filestore_instance_id=None,
                    gcp_filestore_location=None,
                    gcp_cloud_storage_bucket_name=None,
                    memorystore_instance_name=None,
                    functional_verify=None,
                    yes=True,
                )
            if is_managed_cloud:
                e.match("not a cloud with customer defined resources")


def test_get_cloud_resource_value():
    cloud_controller = CloudController()
    cloud_controller.log = Mock()
    cloud_resource = CreateCloudResource(aws_s3_id="old_aws_s3_id",)
    value = cloud_controller._get_cloud_resource_value(cloud_resource, "aws_s3_id")
    assert value == "old_aws_s3_id"
    value = cloud_controller._get_cloud_resource_value(cloud_resource, "aws_efs_id")
    assert value is None


def test_generate_edit_details_logs():
    cloud_controller = CloudController()
    cloud_controller.log = Mock()
    cloud_resource = CreateCloudResource(
        aws_s3_id="old_aws_s3_id",
        aws_efs_id="old_aws_efs_id",
        aws_efs_mount_target_ip="old_aws_efs_mount_target_ip",
    )
    edit_details = {
        "aws_s3_id": "new_aws_s3_id",
        "aws_efs_id": None,
        "aws_efs_mount_target_ip": None,
    }
    detailed_logs = cloud_controller._generate_edit_details_logs(
        cloud_resource, edit_details
    )
    assert detailed_logs == [
        "aws_s3_id: from old_aws_s3_id -> new_aws_s3_id",
    ]

    edit_details = {
        "aws_s3_id": "new_aws_s3_id",
        "aws_efs_id": "new_aws_efs_id",
        "aws_efs_mount_target_ip": "new_aws_efs_mount_target_ip",
    }
    detailed_logs = cloud_controller._generate_edit_details_logs(
        cloud_resource, edit_details
    )
    assert detailed_logs == [
        "aws_s3_id: from old_aws_s3_id -> new_aws_s3_id",
        "aws_efs_id: from old_aws_efs_id -> new_aws_efs_id",
        "aws_efs_mount_target_ip: from old_aws_efs_mount_target_ip -> new_aws_efs_mount_target_ip",
    ]


def test_generate_rollback_command():
    cloud_controller = CloudController()
    cloud_controller.log = Mock()
    cloud_resource = CreateCloudResource(
        aws_s3_id="old_aws_s3_id",
        aws_efs_id="old_aws_efs_id",
        aws_efs_mount_target_ip="old_aws_efs_mount_target_ip",
    )
    edit_details = {
        "aws_s3_id": "new_aws_s3_id",
        "aws_efs_id": None,
        "aws_efs_mount_target_ip": None,
    }
    rollback_command = cloud_controller._generate_rollback_command(
        "fake_cloud_id", cloud_resource, edit_details
    )
    assert (
        rollback_command
        == "anyscale cloud edit --cloud-id=fake_cloud_id --aws-s3-id=old_aws_s3_id"
    )

    edit_details = {
        "aws_s3_id": "new_aws_s3_id",
        "aws_efs_id": "new_aws_efs_id",
        "aws_efs_mount_target_ip": "new_aws_efs_mount_target_ip",
    }
    rollback_command = cloud_controller._generate_rollback_command(
        "fake_cloud_id", cloud_resource, edit_details
    )
    assert (
        rollback_command
        == "anyscale cloud edit --cloud-id=fake_cloud_id --aws-s3-id=old_aws_s3_id --aws-efs-id=old_aws_efs_id --aws-efs-mount-target-ip=old_aws_efs_mount_target_ip"
    )


### End of test edit cloud ###


@pytest.mark.parametrize(
    (
        "is_bring_your_own_resource",
        "no_cfn_stack",
        "has_cloud_resource",
        "cloud_provider",
        "enable_ft",
        "expected_result",
    ),
    [
        pytest.param(False, True, True, "AWS", False, False, id="no-cfn-stack"),
        pytest.param(False, False, False, "AWS", False, False, id="no-cloud-resource"),
        pytest.param(True, False, True, "AWS", False, False, id="not-managed-cloud"),
        pytest.param(None, False, True, "AWS", False, False, id="unknown-cloud-type"),
        pytest.param(False, False, True, "AWS", False, True, id="happy-path-iam"),
        pytest.param(
            False, False, True, "GCP", False, False, id="cloud-provider-mismatch"
        ),
        pytest.param(False, False, True, "AWS", True, True, id="happy-path-redis"),
        pytest.param(False, False, True, "GCP", True, True, id="happy-path-redis"),
    ],
)
def test_update_managed_cloud(
    is_bring_your_own_resource: Optional[bool],
    no_cfn_stack: bool,
    has_cloud_resource: bool,
    enable_ft: bool,
    cloud_provider: str,
    expected_result: bool,
):
    mock_cloud = Mock(
        provider=cloud_provider, is_bring_your_own_resource=is_bring_your_own_resource
    )
    mock_cloud_resource = None
    if has_cloud_resource:
        mock_cloud_resource = Mock(
            aws_cloudformation_stack_id="mock_aws_cloudformation_stack_id"
            if not no_cfn_stack
            else None,
        )
    with patch.multiple(
        "anyscale.controllers.cloud_controller",
        anyscale_version=Mock(return_value="0.0.0-dev"),
        get_cloud_resource_by_cloud_id=Mock(return_value=mock_cloud_resource),
        update_iam_role=Mock(),
    ), patch.multiple(
        "anyscale.controllers.cloud_controller.CloudController",
        _add_redis_cluster_aws=Mock(),
        _add_redis_cluster_gcp=Mock(),
    ):
        cloud_controller = CloudController()
        cloud_controller.api_client.get_cloud_api_v2_clouds_cloud_id_get = Mock(
            return_value=Mock(result=mock_cloud)
        )
        if not expected_result:
            with pytest.raises(ClickException) as e:
                cloud_controller.update_managed_cloud(
                    None, Mock(), enable_ft, None, True
                )
            if is_bring_your_own_resource is None or is_bring_your_own_resource:
                e.match("Cannot update cloud with customer defined resources")
            elif not has_cloud_resource:
                e.match("does not contain resource records")
            elif no_cfn_stack:
                e.match("does not have an associated cloudformation stack")
            elif not enable_ft and cloud_provider == "GCP":
                e.match("Only AWS")
        else:
            cloud_controller.update_managed_cloud(None, Mock(), enable_ft, None, True)


@pytest.mark.parametrize(
    "use_strict_iam_permissions", [True, False],
)
def test_get_anyscale_cross_account_iam_policies(use_strict_iam_permissions: bool):
    mock_cloud_id = "mock_cloud_id"
    mock_parameter = {
        "ParameterKey": "AnyscaleCrossAccountIAMPolicySteadyState",
        "ParameterValue": "mock_iam_policy",
    }
    mock_altered_policy = "mock_iam_policy_altered"
    mock_get_anyscale_cross_account_iam_policies = Mock(return_value=[mock_parameter])
    mock_get_anyscale_iam_permissions_ec2_restricted = Mock(
        return_value=mock_altered_policy
    )
    with patch.multiple(
        "anyscale.controllers.cloud_controller",
        get_anyscale_cross_account_iam_policies=mock_get_anyscale_cross_account_iam_policies,
        get_anyscale_iam_permissions_ec2_restricted=mock_get_anyscale_iam_permissions_ec2_restricted,
    ):
        cloud_controller = CloudController()
        policies = cloud_controller._get_anyscale_cross_account_iam_policies(
            mock_cloud_id, use_strict_iam_permissions
        )
        mock_get_anyscale_cross_account_iam_policies.assert_called_once()
        if use_strict_iam_permissions:
            mock_get_anyscale_iam_permissions_ec2_restricted.assert_called_with(
                mock_cloud_id
            )
            assert policies == [
                {
                    "ParameterKey": mock_parameter["ParameterKey"],
                    "ParameterValue": json.dumps(mock_altered_policy),
                }
            ]
        else:
            mock_get_anyscale_iam_permissions_ec2_restricted.assert_not_called()
            assert policies == [mock_parameter]


@pytest.mark.parametrize(
    ("has_memorystore", "db_update_failed"),
    [
        pytest.param(False, False, id="happy-path"),
        pytest.param(True, False, id="has-memorystore"),
        pytest.param(False, True, id="edit-failed"),
    ],
)
def test_add_redis_cluster_gcp(has_memorystore: bool, db_update_failed: bool, capsys):
    mock_memorystore_name = "mock_memorystore_name"
    mock_cloud = Mock(id="mock_cloud_id")
    mock_cloud_resource = MagicMock(
        memorystore_instance_config=Mock() if has_memorystore else None,
        gcp_deployment_manager_id=Mock(),
    )
    mock_managed_setup_utils = MagicMock(
        get_or_create_memorystore_gcp=Mock(return_value=mock_memorystore_name)
    )
    mock_gcp_utils = MagicMock(
        get_google_cloud_client_factory=Mock(), get_gcp_memorystore_config=Mock()
    )
    with patch.multiple(
        "anyscale.controllers.cloud_controller",
        try_import_gcp_managed_setup_utils=Mock(return_value=mock_managed_setup_utils),
        try_import_gcp_utils=Mock(return_value=mock_gcp_utils),
    ), patch.multiple(
        "anyscale.controllers.cloud_controller.CloudController", _get_project_id=Mock()
    ):
        cloud_controller = CloudController()
        cloud_controller.api_client.edit_cloud_resource_api_v2_clouds_with_cloud_resource_gcp_router_cloud_id_patch = (
            Mock()
            if not db_update_failed
            else Mock(side_effect=ClickException("Edit cloud failed!"))
        )
        if db_update_failed:
            with pytest.raises(ClickException) as e:
                cloud_controller._add_redis_cluster_gcp(mock_cloud, mock_cloud_resource)
            e.match("Cloud update failed!")
        else:
            cloud_controller._add_redis_cluster_gcp(mock_cloud, mock_cloud_resource)
            if has_memorystore:
                _, stdout = capsys.readouterr()
                assert "already exists" in stdout


@pytest.mark.parametrize(
    (
        "memorydb_in_cloud_resource",
        "get_or_create_memorydb_error",
        "edit_cloud_resource_error",
        "expected_error",
    ),
    [
        pytest.param(False, False, False, False, id="happy-path"),
        pytest.param(True, False, False, False, id="memorydb-in-cloud-resource"),
        pytest.param(False, True, False, True, id="get-or-created-memorydb-error"),
        pytest.param(False, False, True, True, id="edit-cloud-resource-error"),
    ],
)
def test_add_redis_cluster_aws(
    memorydb_in_cloud_resource: bool,
    get_or_create_memorydb_error: bool,
    edit_cloud_resource_error: bool,
    expected_error: bool,
):
    mock_cloud = Mock()
    mock_cloud_resource = MagicMock(
        memorydb_cluster_config=MagicMock(id="mock")
        if memorydb_in_cloud_resource
        else None,
        aws_cloudformation_stack_id="mock_aws_cloudformation_stack_id",
        aws_subnet_ids_with_availability_zones=[1, 2],
    )
    mock_get_or_create_memorydb = Mock()
    if get_or_create_memorydb_error:
        mock_get_or_create_memorydb.side_effect = ClickException(
            "Failed to get or create memorydb"
        )
    mock_edit_cloud_resource = Mock()
    if edit_cloud_resource_error:
        mock_edit_cloud_resource.side_effect = ClickException(
            "Failed to edit cloud resource"
        )
    with patch.multiple(
        "anyscale.controllers.cloud_controller",
        get_or_create_memorydb=mock_get_or_create_memorydb,
        _get_memorydb_cluster_config=Mock(),
    ):
        cloud_controller = CloudController()
        cloud_controller.api_client.edit_cloud_resource_api_v2_clouds_with_cloud_resource_router_cloud_id_patch = (
            mock_edit_cloud_resource
        )
        if expected_error:
            with pytest.raises(ClickException) as e:
                cloud_controller._add_redis_cluster_aws(mock_cloud, mock_cloud_resource)
            e.match("Cloud update failed!")
            if get_or_create_memorydb_error:
                mock_get_or_create_memorydb.assert_called_once()
                mock_edit_cloud_resource.assert_not_called()
            elif edit_cloud_resource_error:
                mock_get_or_create_memorydb.assert_called_once()
                mock_edit_cloud_resource.assert_called_once()
        else:
            cloud_controller._add_redis_cluster_aws(mock_cloud, mock_cloud_resource)
            if memorydb_in_cloud_resource:
                mock_get_or_create_memorydb.assert_not_called()
                mock_edit_cloud_resource.assert_not_called()
            else:
                mock_get_or_create_memorydb.assert_called_once()
                mock_edit_cloud_resource.assert_called_once()
