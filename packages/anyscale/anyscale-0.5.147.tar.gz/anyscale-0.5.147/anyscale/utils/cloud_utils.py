import contextlib
from enum import Enum
import sys
from typing import Optional, Tuple
import uuid

import boto3
from botocore.exceptions import ClientError
from click.exceptions import ClickException

from anyscale.cli_logger import CloudSetupLogger
from anyscale.client.openapi_client.api.default_api import DefaultApi
from anyscale.client.openapi_client.models import (
    CloudAnalyticsEvent,
    CloudAnalyticsEventCloudResource,
    CloudAnalyticsEventCommandName,
    CloudAnalyticsEventError,
    CloudAnalyticsEventName,
    CloudProviders,
    CreateAnalyticsEvent,
)
from anyscale.cloud import get_cloud_id_and_name


def get_organization_default_cloud(api_client: DefaultApi) -> Optional[str]:
    """Return default cloud name for organization if it exists and
        if user has correct permissions for it.

        Returns:
            Name of default cloud name for organization if it exists and
            if user has correct permissions for it.
        """
    user = api_client.get_user_info_api_v2_userinfo_get().result
    organization = user.organizations[0]  # Each user only has one org
    if organization.default_cloud_id:
        try:
            # Check permissions
            _, cloud_name = get_cloud_id_and_name(
                api_client, cloud_id=organization.default_cloud_id
            )
            return str(cloud_name)
        except Exception:  # noqa: BLE001
            return None
    return None


def get_default_cloud(
    api_client: DefaultApi, cloud_name: Optional[str]
) -> Tuple[str, str]:
    """Returns the cloud id from cloud name.
    If cloud name is not provided, returns the default cloud name if exists in organization.
    If default cloud name does not exist returns last used cloud.
    """

    if cloud_name is None:
        default_cloud_name = get_organization_default_cloud(api_client)
        if default_cloud_name:
            cloud_name = default_cloud_name
    return get_cloud_id_and_name(api_client, cloud_name=cloud_name)


def verify_anyscale_access(
    api_client: DefaultApi,
    cloud_id: str,
    cloud_provider: CloudProviders,
    logger: CloudSetupLogger,
) -> bool:
    try:
        api_client.verify_access_api_v2_cloudsverify_access_cloud_id_get(cloud_id)
        return True
    except ClickException as e:
        if cloud_provider == CloudProviders.AWS:
            logger.log_resource_error(
                CloudAnalyticsEventCloudResource.AWS_IAM_ROLE,
                CloudSetupError.ANYSCALE_ACCESS_DENIED,
            )
        elif cloud_provider == CloudProviders.GCP:
            logger.log_resource_error(
                CloudAnalyticsEventCloudResource.GCP_SERVICE_ACCOUNT,
                CloudSetupError.ANYSCALE_ACCESS_DENIED,
            )
        logger.error(
            f"Anyscale's control plane is unable to access resources on your cloud provider.\n{e}"
        )
        return False


def modify_memorydb_parameter_group(parameter_group_name: str, region: str) -> None:
    """
    Modify the memorydb parameter group to set the maxmemory-policy to allkeys-lru.

    This is not done in the cloudformation template because we have to create the paramter group first and then modify it.
    """
    try:
        memorydb_client = boto3.client("memorydb", region_name=region)
        memorydb_client.update_parameter_group(
            ParameterGroupName=parameter_group_name,
            ParameterNameValues=[
                {"ParameterName": "maxmemory-policy", "ParameterValue": "allkeys-lru",}
            ],
        )
    except ClientError as e:
        # TODO (allenyin): add memorydb to the cloud provider error list.
        raise ClickException(
            f"Failed to modify memorydb parameter group {parameter_group_name}. Please make sure you have permission to perform UpdateParameterGroup on memorydb clusters and try again. \n{e}"
        )


class CloudSetupError(str, Enum):
    ANYSCALE_ACCESS_DENIED = "ANYSCALE_ACCESS_DENIED"
    RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"
    CIDR_BLOCK_TOO_SMALL = "CIDR_BLOCK_TOO_SMALL"
    MISSING_CLOUD_RESOURCE_ID = "MISSING_CLOUD_RESOURCE_ID"
    ONLY_ONE_SUBNET = "ONLY_ONE_SUBNET"
    SUBNET_NOT_IN_VPC = "SUBNET_NOT_IN_VPC"
    ONLY_ONE_AZ = "ONLY_ONE_AZ"
    IAM_ROLE_ACCOUNT_MISMATCH = "IAM_ROLE_ACCOUNT_MISMATCH"
    INSTANCE_PROFILE_NOT_FOUND = "INSTANCE_PROFILE_NOT_FOUND"
    INTERNAL_COMMUNICATION_NOT_ALLOWED = "INTERNAL_COMMUNICATION_NOT_ALLOWED"
    MALFORMED_CORS_RULE = "MALFORMED_CORS_RULE"
    INCORRECT_CORS_RULE = "INCORRECT_CORS_RULE"
    MOUNT_TARGET_NOT_FOUND = "MOUNT_TARGET_NOT_FOUND"
    INVALID_MOUNT_TARGET = "INVALID_MOUNT_TARGET"
    PROJECT_NOT_ACTIVE = "PROJECT_NOT_ACTIVE"
    API_NOT_ENABLED = "API_NOT_ENABLED"
    FIREWALL_NOT_ASSOCIATED_WITH_VPC = "FIREWALL_NOT_ASSOCIATED_WITH_VPC"
    FILESTORE_NAME_MALFORMED = "FILESTORE_NAME_MALFORMED"
    FILESTORE_NOT_CONNECTED_TO_VPC = "FILESTORE_NOT_CONNECTED_TO_VPC"
    MEMORYSTORE_NOT_CONNECTED_TO_VPC = "MEMORYSTORE_NOT_CONNECTED_TO_VPC"
    MEMORYSTORE_READ_REPLICAS_DISABLED = "MEMORYSTORE_READ_REPLICAS_DISABLED"
    MEMORYDB_CLUSTER_UNAVAILABLE = "MEMORYDB_CLUSTER_UNAVAILABLE"


class CloudEventProducer:
    """
    Produce events during cloud setup/register/verify
    """

    def __init__(self, api_client: DefaultApi):
        self.api_client = api_client
        self.cloud_id: Optional[str] = None
        self.cloud_provider: Optional[CloudProviders] = None

    def init_trace_context(
        self,
        command_name: CloudAnalyticsEventCommandName,
        cloud_provider: CloudProviders,
        cloud_id: Optional[str] = None,
    ):
        self.trace_id = str(uuid.uuid4().hex)
        self.command_name = command_name
        self.raw_command_input = str(" ".join(sys.argv[1:]))
        self.cloud_id = cloud_id
        self.cloud_provider = cloud_provider

    def set_cloud_id(self, cloud_id: str):
        self.cloud_id = cloud_id

    def produce(
        self,
        event_name: CloudAnalyticsEventName,
        succeeded: bool,
        logger: Optional[CloudSetupLogger] = None,
        internal_error: Optional[str] = None,
    ):
        with contextlib.suppress(Exception):
            # shouldn't block cloud setup even if cloud event generation fails
            error = None
            if not succeeded:
                cloud_provider_error = None
                if logger:
                    cloud_provider_error_list = logger.get_cloud_provider_errors()
                    logger.clear_cloud_provider_errors()
                    if len(cloud_provider_error_list) > 0:
                        cloud_provider_error = cloud_provider_error_list
                error = CloudAnalyticsEventError(
                    internal_error=internal_error,
                    cloud_provider_error=cloud_provider_error,
                )

            self.api_client.produce_analytics_event_api_v2_analytics_post(
                CreateAnalyticsEvent(
                    cloud_analytics_event=CloudAnalyticsEvent(
                        trace_id=self.trace_id,
                        cloud_id=self.cloud_id,
                        succeeded=succeeded,
                        command_name=self.command_name,
                        raw_command_input=self.raw_command_input,
                        cloud_provider=self.cloud_provider,
                        event_name=event_name,
                        error=error,
                    )
                )
            )
