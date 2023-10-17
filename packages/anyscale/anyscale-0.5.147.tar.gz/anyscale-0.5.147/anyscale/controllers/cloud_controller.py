"""
Fetches data required and formats output for `anyscale cloud` commands.
"""

import copy
from datetime import timedelta
import json
from os import getenv
import re
import secrets
import time
from typing import Any, Dict, List, Optional, Tuple

import boto3
from botocore.exceptions import ClientError, NoCredentialsError
import click
from click import ClickException

from anyscale import __version__ as anyscale_version
from anyscale.aws_iam_policies import get_anyscale_iam_permissions_ec2_restricted
from anyscale.cli_logger import CloudSetupLogger
from anyscale.client.openapi_client.models import (
    AWSMemoryDBClusterConfig,
    CloudAnalyticsEventCloudResource,
    CloudAnalyticsEventCommandName,
    CloudAnalyticsEventName,
    CloudProviders,
    CloudState,
    CloudWithCloudResource,
    CloudWithCloudResourceGCP,
    ClusterManagementStackVersions,
    CreateCloudResource,
    CreateCloudResourceGCP,
    EditableCloudResource,
    EditableCloudResourceGCP,
    SubnetIdWithAvailabilityZoneAWS,
    UpdateCloudWithCloudResource,
    UpdateCloudWithCloudResourceGCP,
    WriteCloud,
)
from anyscale.client.openapi_client.models.gcp_file_store_config import (
    GCPFileStoreConfig,
)
from anyscale.cloud import (
    get_cloud_id_and_name,
    get_cloud_json_from_id,
    get_cloud_resource_by_cloud_id,
    get_organization_id,
)
from anyscale.cloud_resource import (
    associate_aws_subnets_with_azs,
    verify_aws_cloudformation_stack,
    verify_aws_efs,
    verify_aws_iam_roles,
    verify_aws_memorydb_cluster,
    verify_aws_s3,
    verify_aws_security_groups,
    verify_aws_subnets,
    verify_aws_vpc,
)
from anyscale.conf import ANYSCALE_IAM_ROLE_NAME
from anyscale.controllers.base_controller import BaseController
from anyscale.controllers.cloud_functional_verification_controller import (
    CloudFunctionalVerificationController,
    CloudFunctionalVerificationType,
)
from anyscale.formatters import clouds_formatter
from anyscale.shared_anyscale_utils.aws import AwsRoleArn
from anyscale.shared_anyscale_utils.conf import ANYSCALE_ENV
from anyscale.util import (  # pylint:disable=private-import
    _client,
    _get_aws_efs_mount_target_ip,
    _get_memorydb_cluster_config,
    _get_role,
    _update_external_ids_for_policy,
    confirm,
    GCP_DEPLOYMENT_MANAGER_TIMEOUT_SECONDS_LONG,
    get_anyscale_cross_account_iam_policies,
    get_available_regions,
    get_user_env_aws_account,
    prepare_cloudformation_template,
    REDIS_TLS_ADDRESS_PREFIX,
)
from anyscale.utils.cloud_update_utils import (
    CLOUDFORMATION_TIMEOUT_SECONDS_LONG,
    get_or_create_memorydb,
    MEMORYDB_REDIS_PORT,
    try_delete_customer_drifts_policy,
    update_iam_role,
)
from anyscale.utils.cloud_utils import (
    CloudEventProducer,
    CloudSetupError,
    modify_memorydb_parameter_group,
    verify_anyscale_access,
)
from anyscale.utils.imports.gcp import (
    try_import_gcp_managed_setup_utils,
    try_import_gcp_utils,
    try_import_gcp_verify_lib,
)


ROLE_CREATION_RETRIES = 30
ROLE_CREATION_INTERVAL_SECONDS = 1

try:
    CLOUDFORMATION_TIMEOUT_SECONDS = int(getenv("CLOUDFORMATION_TIMEOUT_SECONDS", 300))
except ValueError:
    raise Exception(
        f"CLOUDFORMATION_TIMEOUT_SECONDS is set to {getenv('CLOUDFORMATION_TIMEOUT_SECONDS')}, which is not a valid integer."
    )


try:
    GCP_DEPLOYMENT_MANAGER_TIMEOUT_SECONDS = int(
        getenv("GCP_DEPLOYMENT_MANAGER_TIMEOUT_SECONDS", 300)
    )
except ValueError:
    raise Exception(
        f"GCP_DEPLOYMENT_MANAGER_TIMEOUT_SECONDS is set to {getenv('GCP_DEPLOYMENT_MANAGER_TIMEOUT_SECONDS')}, which is not a valid integer."
    )

IGNORE_CAPACITY_ERRORS = getenv("IGNORE_CAPACITY_ERRORS") is not None

# Constants forked from ray.autoscaler._private.aws.config
RAY = "ray-autoscaler"
DEFAULT_RAY_IAM_ROLE = RAY + "-v1"

# Only used in cloud edit.
BASE_ROLLBACK_COMMAND = "anyscale cloud edit --cloud-id={cloud_id}"


class CloudController(BaseController):
    def __init__(
        self,
        log: Optional[CloudSetupLogger] = None,
        initialize_auth_api_client: bool = True,
    ):
        if log is None:
            log = CloudSetupLogger()

        super().__init__(initialize_auth_api_client=initialize_auth_api_client)
        self.log = log
        self.log.open_block("Output")

        self.cloud_event_producer = CloudEventProducer(api_client=self.api_client)

    def list_clouds(self, cloud_name: Optional[str], cloud_id: Optional[str]) -> str:
        if cloud_id is not None:
            clouds = [
                self.api_client.get_cloud_api_v2_clouds_cloud_id_get(cloud_id).result
            ]
        elif cloud_name is not None:
            clouds = [
                self.api_client.find_cloud_by_name_api_v2_clouds_find_by_name_post(
                    {"name": cloud_name}
                ).result
            ]
        else:
            clouds = self.api_client.list_clouds_api_v2_clouds_get().results
        output = clouds_formatter.format_clouds_output(clouds=clouds, json_format=False)

        return str(output)

    def _get_anyscale_cross_account_iam_policies(
        self, cloud_id: str, _use_strict_iam_permissions: bool,
    ) -> List[Dict[str, str]]:
        iam_policy_parameters = get_anyscale_cross_account_iam_policies()
        if _use_strict_iam_permissions:
            anyscale_iam_permissions_ec2 = get_anyscale_iam_permissions_ec2_restricted(
                cloud_id
            )
            for parameter in iam_policy_parameters:
                if (
                    parameter["ParameterKey"]
                    == "AnyscaleCrossAccountIAMPolicySteadyState"
                ):
                    parameter["ParameterValue"] = json.dumps(
                        anyscale_iam_permissions_ec2
                    )
                    break
        return iam_policy_parameters

    def run_cloudformation(
        self,
        region: str,
        cloud_id: str,
        anyscale_iam_role_name: str,
        cluster_node_iam_role_name: str,
        enable_head_node_fault_tolerance: bool,
        _use_strict_iam_permissions: bool = False,  # This should only be used in testing.
    ) -> Dict[str, Any]:
        """
        Run cloudformation to create the AWS resources for a cloud.

        When enable_head_node_fault_tolerance is set to True, a memorydb cluster will be created.
        """
        response = (
            self.api_client.get_anyscale_aws_account_api_v2_clouds_anyscale_aws_account_get()
        )

        anyscale_aws_account = response.result.anyscale_aws_account
        cfn_client = _client("cloudformation", region)
        cfn_stack_name = cloud_id.replace("_", "-").lower()

        cfn_template_body = prepare_cloudformation_template(
            region, cfn_stack_name, cloud_id, enable_head_node_fault_tolerance
        )

        cross_account_iam_policies = self._get_anyscale_cross_account_iam_policies(
            cloud_id, _use_strict_iam_permissions
        )

        parameters = [
            {"ParameterKey": "EnvironmentName", "ParameterValue": ANYSCALE_ENV},
            {"ParameterKey": "AnyscaleCLIVersion", "ParameterValue": anyscale_version},
            {"ParameterKey": "CloudID", "ParameterValue": cloud_id},
            {
                "ParameterKey": "AnyscaleAWSAccountID",
                "ParameterValue": anyscale_aws_account,
            },
            {
                "ParameterKey": "AnyscaleCrossAccountIAMRoleName",
                "ParameterValue": anyscale_iam_role_name,
            },
            {
                "ParameterKey": "ClusterNodeIAMRoleName",
                "ParameterValue": cluster_node_iam_role_name,
            },
            {
                "ParameterKey": "MemoryDBRedisPort",
                "ParameterValue": MEMORYDB_REDIS_PORT,
            },
        ]
        for parameter in cross_account_iam_policies:
            parameters.append(parameter)

        self.log.debug("cloudformation body:")
        self.log.debug(cfn_template_body)

        cfn_client.create_stack(
            StackName=cfn_stack_name,
            TemplateBody=cfn_template_body,
            Parameters=parameters,
            Capabilities=["CAPABILITY_NAMED_IAM", "CAPABILITY_AUTO_EXPAND"],
        )

        stacks = cfn_client.describe_stacks(StackName=cfn_stack_name)
        cfn_stack = stacks["Stacks"][0]
        cfn_stack_url = f"https://{region}.console.aws.amazon.com/cloudformation/home?region={region}#/stacks/stackinfo?stackId={cfn_stack['StackId']}"
        self.log.info(f"\nTrack progress of cloudformation at {cfn_stack_url}")
        with self.log.spinner("Creating cloud resources through cloudformation..."):
            start_time = time.time()
            end_time = (
                start_time + CLOUDFORMATION_TIMEOUT_SECONDS_LONG
                if enable_head_node_fault_tolerance
                else start_time + CLOUDFORMATION_TIMEOUT_SECONDS
            )
            while time.time() < end_time:
                stacks = cfn_client.describe_stacks(StackName=cfn_stack_name)
                cfn_stack = stacks["Stacks"][0]
                if cfn_stack["StackStatus"] in (
                    "CREATE_FAILED",
                    "ROLLBACK_COMPLETE",
                    "ROLLBACK_IN_PROGRESS",
                ):
                    bucket_name = f"anyscale-{ANYSCALE_ENV}-data-{cfn_stack_name}"
                    try:
                        _client("s3", region).delete_bucket(Bucket=bucket_name)
                        self.log.info(f"Successfully deleted {bucket_name}")
                    except Exception as e:  # noqa: BLE001
                        if not (
                            isinstance(e, ClientError)
                            and e.response["Error"]["Code"] == "NoSuchBucket"
                        ):
                            self.log.error(
                                f"Unable to delete the S3 bucket created by the cloud formation stack, please manually delete {bucket_name}"
                            )

                    # Provide link to cloudformation
                    self.cloud_event_producer.produce(
                        CloudAnalyticsEventName.RESOURCES_CREATED, succeeded=False,
                    )
                    raise ClickException(
                        f"Failed to set up cloud resources. Please check your cloudformation stack for errors and to ensure that all resources created in this cloudformation stack were deleted: {cfn_stack_url}"
                    )
                if cfn_stack["StackStatus"] == "CREATE_COMPLETE":
                    if enable_head_node_fault_tolerance:
                        modify_memorydb_parameter_group(cfn_stack_name, region)
                    self.log.info(
                        f"Cloudformation stack {cfn_stack['StackId']} Completed"
                    )
                    break

                time.sleep(1)

            if time.time() > end_time:
                self.cloud_event_producer.produce(
                    CloudAnalyticsEventName.RESOURCES_CREATED,
                    succeeded=False,
                    internal_error="Cloudformation timed out.",
                )
                raise ClickException(
                    f"Timed out creating AWS resources. Please check your cloudformation stack for errors. {cfn_stack['StackId']}"
                )
        self.cloud_event_producer.produce(
            CloudAnalyticsEventName.RESOURCES_CREATED, succeeded=True,
        )
        return cfn_stack

    def run_deployment_manager(  # noqa: PLR0913
        self,
        factory: Any,
        deployment_name: str,
        cloud_id: str,
        project_id: str,
        region: str,
        anyscale_access_service_account: str,
        workload_identity_pool_name: str,
        anyscale_aws_account: str,
        organization_id: str,
        enable_head_node_fault_tolerance: bool,
    ):
        setup_utils = try_import_gcp_managed_setup_utils()

        anyscale_access_service_account_name = anyscale_access_service_account.split(
            "@"
        )[0]
        deployment_config = setup_utils.generate_deployment_manager_config(
            region,
            project_id,
            cloud_id,
            anyscale_access_service_account_name,
            workload_identity_pool_name,
            anyscale_aws_account,
            organization_id,
            enable_head_node_fault_tolerance,
        )

        self.log.debug("GCP Deployment Manager resource config:")
        self.log.debug(deployment_config)

        deployment = {
            "name": deployment_name,
            "target": {"config": {"content": deployment_config,},},
        }

        deployment_client = factory.build("deploymentmanager", "v2")
        response = (
            deployment_client.deployments()
            .insert(project=project_id, body=deployment)
            .execute()
        )
        deployment_url = f"https://console.cloud.google.com/dm/deployments/details/{deployment_name}?project={project_id}"

        timeout_seconds = (
            GCP_DEPLOYMENT_MANAGER_TIMEOUT_SECONDS_LONG
            if enable_head_node_fault_tolerance
            else GCP_DEPLOYMENT_MANAGER_TIMEOUT_SECONDS
        )
        self.log.info(
            f"Note that it may take up to {int(timeout_seconds / 60)} minutes to create resources on GCP."
        )
        self.log.info(f"Track progress of Deployment Manager at {deployment_url}")
        with self.log.spinner("Creating cloud resources through Deployment Manager..."):
            start_time = time.time()
            end_time = start_time + timeout_seconds
            while time.time() < end_time:
                current_operation = (
                    deployment_client.operations()
                    .get(operation=response["name"], project=project_id)
                    .execute()
                )
                if current_operation.get("status", None) == "DONE":
                    if "error" in current_operation:
                        self.log.error(f"Error: {current_operation['error']}")
                        raise ClickException(
                            f"Failed to set up cloud resources. Please check your Deployment Manager for errors and delete all resources created in this deployment: {deployment_url}"
                        )
                    # happy path
                    self.log.info("Deployment succeeded.")
                    return True
                time.sleep(1)
            # timeout
            raise ClickException(
                f"Timed out creating GCP resources. Please check your deployment for errors and delete all resources created in this deployment: {deployment_url}"
            )

    def update_cloud_with_resources(
        self,
        cfn_stack: Dict[str, Any],
        cloud_id: str,
        enable_head_node_fault_tolerance: bool,
    ):
        if "Outputs" not in cfn_stack:
            raise ClickException(
                f"Timed out setting up cloud resources. Please check your cloudformation stack for errors. {cfn_stack['StackId']}"
            )

        cfn_resources = {}
        for resource in cfn_stack["Outputs"]:
            resource_type = resource["OutputKey"]
            resource_value = resource["OutputValue"]
            assert (
                resource_value is not None
            ), f"{resource_type} is not created properly. Please delete the cloud and try creating agian."
            cfn_resources[resource_type] = resource_value

        aws_subnets_with_availability_zones = json.loads(
            cfn_resources["SubnetsWithAvailabilityZones"]
        )
        aws_vpc_id = cfn_resources["VPC"]
        aws_security_groups = [cfn_resources["AnyscaleSecurityGroup"]]
        aws_s3_id = cfn_resources["S3Bucket"]
        aws_efs_id = cfn_resources["EFS"]
        aws_efs_mount_target_ip = cfn_resources["EFSMountTargetIP"]
        anyscale_iam_role_arn = cfn_resources["AnyscaleIAMRole"]
        cluster_node_iam_role_arn = cfn_resources["NodeIamRole"]

        if enable_head_node_fault_tolerance:
            memorydb = json.loads(cfn_resources["MemoryDB"])
            memorydb_cluster_config = AWSMemoryDBClusterConfig(
                id=memorydb["arn"],
                endpoint=f'{REDIS_TLS_ADDRESS_PREFIX}{memorydb["ClusterEndpointAddress"]}:{MEMORYDB_REDIS_PORT}',
            )
        else:
            memorydb_cluster_config = None

        create_cloud_resource = CreateCloudResource(
            aws_vpc_id=aws_vpc_id,
            aws_subnet_ids_with_availability_zones=[
                SubnetIdWithAvailabilityZoneAWS(
                    subnet_id=subnet_with_az["subnet_id"],
                    availability_zone=subnet_with_az["availability_zone"],
                )
                for subnet_with_az in aws_subnets_with_availability_zones
            ],
            aws_iam_role_arns=[anyscale_iam_role_arn, cluster_node_iam_role_arn],
            aws_security_groups=aws_security_groups,
            aws_s3_id=aws_s3_id,
            aws_efs_id=aws_efs_id,
            aws_efs_mount_target_ip=aws_efs_mount_target_ip,
            aws_cloudformation_stack_id=cfn_stack["StackId"],
            memorydb_cluster_config=memorydb_cluster_config,
        )
        with self.log.spinner("Updating Anyscale cloud with cloud resources..."):
            self.api_client.update_cloud_with_cloud_resource_api_v2_clouds_with_cloud_resource_router_cloud_id_put(
                cloud_id=cloud_id,
                update_cloud_with_cloud_resource=UpdateCloudWithCloudResource(
                    cloud_resource_to_update=create_cloud_resource
                ),
            )

    def update_cloud_with_resources_gcp(
        self,
        factory: Any,
        deployment_name: str,
        cloud_id: str,
        project_id: str,
        anyscale_access_service_account: str,
    ):
        setup_utils = try_import_gcp_managed_setup_utils()
        gcp_utils = try_import_gcp_utils()
        anyscale_access_service_account_name = anyscale_access_service_account.split(
            "@"
        )[0]

        cloud_resources = setup_utils.get_deployment_resources(
            factory, deployment_name, project_id, anyscale_access_service_account_name
        )
        gcp_vpc_id = cloud_resources["compute.v1.network"]
        gcp_subnet_ids = [cloud_resources["compute.v1.subnetwork"]]
        gcp_cluster_node_service_account_email = f'{cloud_resources["iam.v1.serviceAccount"]}@{anyscale_access_service_account.split("@")[-1]}'
        gcp_anyscale_iam_service_account_email = anyscale_access_service_account
        gcp_firewall_policy = cloud_resources[
            "gcp-types/compute-v1:networkFirewallPolicies"
        ]
        gcp_firewall_policy_ids = [gcp_firewall_policy]
        gcp_cloud_storage_bucket_id = cloud_resources["storage.v1.bucket"]
        gcp_deployment_manager_id = deployment_name

        gcp_filestore_config = gcp_utils.get_gcp_filestore_config(
            factory,
            project_id,
            gcp_vpc_id,
            cloud_resources["filestore_location"],
            cloud_resources["filestore_instance"],
            self.log,
        )
        memorystore_instance_config = gcp_utils.get_gcp_memorystore_config(
            factory, cloud_resources.get("memorystore_name"),
        )
        try:
            setup_utils.configure_firewall_policy(
                factory, gcp_vpc_id, project_id, gcp_firewall_policy
            )

            create_cloud_resource_gcp = CreateCloudResourceGCP(
                gcp_vpc_id=gcp_vpc_id,
                gcp_subnet_ids=gcp_subnet_ids,
                gcp_cluster_node_service_account_email=gcp_cluster_node_service_account_email,
                gcp_anyscale_iam_service_account_email=gcp_anyscale_iam_service_account_email,
                gcp_filestore_config=gcp_filestore_config,
                gcp_firewall_policy_ids=gcp_firewall_policy_ids,
                gcp_cloud_storage_bucket_id=gcp_cloud_storage_bucket_id,
                gcp_deployment_manager_id=gcp_deployment_manager_id,
                memorystore_instance_config=memorystore_instance_config,
            )
            self.api_client.update_cloud_with_cloud_resource_api_v2_clouds_with_cloud_resource_gcp_router_cloud_id_put(
                cloud_id=cloud_id,
                update_cloud_with_cloud_resource_gcp=UpdateCloudWithCloudResourceGCP(
                    cloud_resource_to_update=create_cloud_resource_gcp,
                ),
            )
        except Exception as e:  # noqa: BLE001
            self.log.error(str(e))
            setup_utils.remove_firewall_policy_associations(
                factory, project_id, gcp_vpc_id
            )
            raise ClickException(
                f"Error occurred when updating resources for the cloud {cloud_id}."
            )

    def prepare_for_managed_cloud_setup(
        self,
        region: str,
        cloud_name: str,
        cluster_management_stack_version: ClusterManagementStackVersions,
    ) -> Tuple[str, str]:
        regions_available = get_available_regions()
        if region not in regions_available:
            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.PREPROCESS_COMPLETE,
                succeeded=False,
                internal_error=f"Region '{region}' is not available.",
            )
            raise ClickException(
                f"Region '{region}' is not available. Regions available are: "
                f"{', '.join(map(repr, regions_available))}"
            )

        for _ in range(5):
            anyscale_iam_role_name = "{}-{}".format(
                ANYSCALE_IAM_ROLE_NAME, secrets.token_hex(4)
            )

            role = _get_role(anyscale_iam_role_name, region)
            if role is None:
                break
        else:
            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.PREPROCESS_COMPLETE,
                succeeded=False,
                internal_error="Unable to find an available AWS IAM Role name",
            )
            raise ClickException(
                "We weren't able to connect your account with the Anyscale because we weren't able to find an available IAM Role name in your account. Please reach out to support or your SA for assistance."
            )

        user_aws_account_id = get_user_env_aws_account(region)
        self.cloud_event_producer.produce(
            CloudAnalyticsEventName.PREPROCESS_COMPLETE, succeeded=True,
        )
        try:
            created_cloud = self.api_client.create_cloud_api_v2_clouds_post(
                write_cloud=WriteCloud(
                    provider="AWS",
                    region=region,
                    credentials=AwsRoleArn.from_role_name(
                        user_aws_account_id, anyscale_iam_role_name
                    ).to_string(),
                    name=cloud_name,
                    is_bring_your_own_resource=False,
                    cluster_management_stack_version=cluster_management_stack_version,
                )
            ).result
            self.cloud_event_producer.set_cloud_id(created_cloud.id)
            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.CLOUD_RECORD_INSERTED, succeeded=True,
            )
        except ClickException as e:
            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.CLOUD_RECORD_INSERTED,
                succeeded=False,
                internal_error=str(e),
            )
            if "409" in e.message:
                raise ClickException(
                    f"Cloud with name {cloud_name} already exists. Please choose a different name."
                )
            raise

        return anyscale_iam_role_name, created_cloud.id

    def prepare_for_managed_cloud_setup_gcp(
        self,
        project_id: str,
        region: str,
        cloud_name: str,
        factory: Any,
        cluster_management_stack_version: ClusterManagementStackVersions,
    ) -> Tuple[str, str, str]:
        setup_utils = try_import_gcp_managed_setup_utils()

        # choose an service account name and create a provider pool
        for _ in range(5):
            token = secrets.token_hex(4)
            anyscale_access_service_account = (
                f"anyscale-access-{token}@{project_id}.iam.gserviceaccount.com"
            )
            service_account = setup_utils.get_anyscale_gcp_access_service_acount(
                factory, anyscale_access_service_account
            )
            if service_account is not None:
                continue
            pool_id = f"anyscale-provider-pool-{token}"
            wordload_identity_pool = setup_utils.get_workload_identity_pool(
                factory, project_id, pool_id
            )
            if wordload_identity_pool is None:
                break
        else:
            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.PREPROCESS_COMPLETE,
                succeeded=False,
                internal_error="Unable to find an available GCP service account name and create a provider pool.",
            )
            raise ClickException(
                "We weren't able to connect your account with the Anyscale because we weren't able to find an available service account name and create a provider pool in your GCP project. Please reach out to support or your SA for assistance."
            )

        # build credentials
        project_number = setup_utils.get_project_number(factory, project_id)
        provider_id = "anyscale-access"
        pool_name = f"{project_number}/locations/global/workloadIdentityPools/{pool_id}"
        provider_name = f"{pool_name}/providers/{provider_id}"
        credentials = json.dumps(
            {
                "project_id": project_id,
                "provider_id": provider_name,
                "service_account_email": anyscale_access_service_account,
            }
        )
        self.cloud_event_producer.produce(
            CloudAnalyticsEventName.PREPROCESS_COMPLETE, succeeded=True,
        )

        # create a cloud
        try:
            created_cloud = self.api_client.create_cloud_api_v2_clouds_post(
                write_cloud=WriteCloud(
                    provider="GCP",
                    region=region,
                    credentials=credentials,
                    name=cloud_name,
                    is_bring_your_own_resource=False,
                    cluster_management_stack_version=cluster_management_stack_version,
                )
            ).result
            self.cloud_event_producer.set_cloud_id(created_cloud.id)
            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.CLOUD_RECORD_INSERTED, succeeded=True,
            )
        except ClickException as e:
            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.CLOUD_RECORD_INSERTED,
                succeeded=False,
                internal_error=str(e),
            )
            if "409" in e.message:
                raise ClickException(
                    f"Cloud with name {cloud_name} already exists. Please choose a different name."
                )
            raise
        return anyscale_access_service_account, pool_name, created_cloud.id

    def create_workload_identity_federation_provider(
        self,
        factory: Any,
        project_id: str,
        pool_id: str,
        anyscale_access_service_account: str,
    ):
        setup_utils = try_import_gcp_managed_setup_utils()
        # create provider pool
        pool_display_name = "Anyscale provider pool"
        pool_description = f"Workload Identity Provider Pool for Anyscale access service account {anyscale_access_service_account}"

        wordload_identity_pool = setup_utils.create_workload_identity_pool(
            factory, project_id, pool_id, self.log, pool_display_name, pool_description,
        )
        try:
            # create provider
            provider_display_name = "Anyscale Access"
            provider_id = "anyscale-access"
            anyscale_aws_account = (
                self.api_client.get_anyscale_aws_account_api_v2_clouds_anyscale_aws_account_get().result.anyscale_aws_account
            )
            organization_id = get_organization_id(self.api_client)
            setup_utils.create_anyscale_aws_provider(
                factory,
                organization_id,
                wordload_identity_pool,
                provider_id,
                anyscale_aws_account,
                provider_display_name,
                self.log,
            )
        except ClickException as e:
            # delete provider pool if there's an exception
            setup_utils.delete_workload_identity_pool(
                factory, wordload_identity_pool, self.log
            )
            raise ClickException(
                f"Error occurred when trying to set up workload identity federation: {e}"
            )

    def wait_for_cloud_to_be_active(self, cloud_id: str) -> None:
        """
        Waits for the cloud to be active
        """
        with self.log.spinner("Setting up resources on Anyscale for your new cloud..."):
            try:
                # This call will get or create the provider metadata for the cloud.
                # Note that this is a blocking call and can take over 60s to complete. This is because we're currently fetching cloud
                # provider metadata in every region, which isn't necessary for cloud setup.
                # TODO (allen): only fetch the provider metadata for the region that the cloud is in.
                self.api_client.get_provider_metadata_api_v2_clouds_provider_metadata_cloud_id_get(
                    cloud_id, max_staleness=int(timedelta(hours=1).total_seconds()),
                )
            except Exception as e:  # noqa: BLE001
                self.log.error(
                    f"Failed to get cloud provider metadata. Your cloud may not be set up properly. Please reach out to Anyscale support for assistance. Error: {e}"
                )

    def setup_managed_cloud(  # noqa: PLR0912
        self,
        *,
        provider: str,
        region: str,
        name: str,
        functional_verify: Optional[str],
        cluster_management_stack_version: ClusterManagementStackVersions,
        enable_head_node_fault_tolerance: bool,
        project_id: str = None,
        yes: bool = False,
        _use_strict_iam_permissions: bool = False,  # This should only be used in testing.
    ) -> None:
        """
        Sets up a cloud provider
        """
        # TODO (congding): split this function into smaller functions per cloud provider
        functions_to_verify = self._validate_functional_verification_args(
            functional_verify
        )
        if provider == "aws":
            self.cloud_event_producer.init_trace_context(
                CloudAnalyticsEventCommandName.SETUP, CloudProviders.AWS
            )
            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.COMMAND_START, succeeded=True,
            )
            with self.log.spinner("Preparing environment for cloud setup..."):
                (
                    anyscale_iam_role_name,
                    cloud_id,
                ) = self.prepare_for_managed_cloud_setup(
                    region, name, cluster_management_stack_version
                )

            try:
                cfn_stack = self.run_cloudformation(
                    region,
                    cloud_id,
                    anyscale_iam_role_name,
                    f"{cloud_id}-cluster_node_role",
                    enable_head_node_fault_tolerance,
                    _use_strict_iam_permissions=_use_strict_iam_permissions,
                )
            except Exception as e:  # noqa: BLE001
                self.log.error(str(e))
                self.api_client.delete_cloud_api_v2_clouds_cloud_id_delete(
                    cloud_id=cloud_id
                )
                raise ClickException("Cloud setup failed!")

            try:
                self.update_cloud_with_resources(
                    cfn_stack, cloud_id, enable_head_node_fault_tolerance
                )
                self.wait_for_cloud_to_be_active(cloud_id)
                self.cloud_event_producer.produce(
                    CloudAnalyticsEventName.INFRA_SETUP_COMPLETE, succeeded=True,
                )
            except Exception as e:  # noqa: BLE001
                self.cloud_event_producer.produce(
                    CloudAnalyticsEventName.INFRA_SETUP_COMPLETE,
                    succeeded=False,
                    internal_error=str(e),
                )
                self.log.error(str(e))
                self.api_client.delete_cloud_api_v2_clouds_cloud_id_delete(
                    cloud_id=cloud_id
                )
                raise ClickException("Cloud setup failed!")

            self.log.info(f"Successfully created cloud {name}, and it's ready to use.")
        elif provider == "gcp":
            if project_id is None:
                raise click.ClickException("Please provide a value for --project-id")
            gcp_utils = try_import_gcp_utils()
            setup_utils = try_import_gcp_managed_setup_utils()
            factory = gcp_utils.get_google_cloud_client_factory(self.log, project_id)
            self.cloud_event_producer.init_trace_context(
                CloudAnalyticsEventCommandName.SETUP, CloudProviders.GCP
            )
            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.COMMAND_START, succeeded=True,
            )
            with self.log.spinner("Preparing environment for cloud setup..."):
                try:
                    organization_id = get_organization_id(self.api_client)
                    anyscale_aws_account = (
                        self.api_client.get_anyscale_aws_account_api_v2_clouds_anyscale_aws_account_get().result.anyscale_aws_account
                    )
                    # Enable APIs in the given GCP project
                    setup_utils.enable_project_apis(factory, project_id, self.log)
                    # We need the Google APIs Service Agent to have security admin permissions on the project
                    # so that we can set IAM policy on Anyscale access service account
                    project_number = setup_utils.get_project_number(
                        factory, project_id
                    ).split("/")[-1]
                    google_api_service_agent = f"serviceAccount:{project_number}@cloudservices.gserviceaccount.com"
                    setup_utils.append_project_iam_policy(
                        factory,
                        project_id,
                        "roles/iam.securityAdmin",
                        google_api_service_agent,
                    )

                except ClickException as e:
                    self.cloud_event_producer.produce(
                        CloudAnalyticsEventName.PREPROCESS_COMPLETE,
                        succeeded=False,
                        logger=self.log,
                        internal_error=str(e),
                    )
                    self.log.error(str(e))
                    raise ClickException("Cloud setup failed!")

                (
                    anyscale_access_service_account,
                    pool_name,
                    cloud_id,
                ) = self.prepare_for_managed_cloud_setup_gcp(
                    project_id, region, name, factory, cluster_management_stack_version
                )

            pool_id = pool_name.split("/")[-1]
            deployment_name = cloud_id.replace("_", "-").lower()
            deployment_succeed = False
            try:
                with self.log.spinner(
                    "Creating workload identity federation provider for Anyscale access..."
                ):
                    self.create_workload_identity_federation_provider(
                        factory, project_id, pool_id, anyscale_access_service_account
                    )
                deployment_succeed = self.run_deployment_manager(
                    factory,
                    deployment_name,
                    cloud_id,
                    project_id,
                    region,
                    anyscale_access_service_account,
                    pool_name,
                    anyscale_aws_account,
                    organization_id,
                    enable_head_node_fault_tolerance,
                )
                self.cloud_event_producer.produce(
                    CloudAnalyticsEventName.RESOURCES_CREATED, succeeded=True,
                )
            except Exception as e:  # noqa: BLE001
                self.cloud_event_producer.produce(
                    CloudAnalyticsEventName.RESOURCES_CREATED, succeeded=False,
                )
                self.log.error(str(e))
                self.api_client.delete_cloud_api_v2_clouds_cloud_id_delete(
                    cloud_id=cloud_id
                )
                setup_utils.delete_workload_identity_pool(factory, pool_name, self.log)
                raise ClickException("Cloud setup failed!")

            try:
                with self.log.spinner(
                    "Updating Anyscale cloud with cloud resources..."
                ):
                    self.update_cloud_with_resources_gcp(
                        factory,
                        deployment_name,
                        cloud_id,
                        project_id,
                        anyscale_access_service_account,
                    )
                self.wait_for_cloud_to_be_active(cloud_id)
                self.cloud_event_producer.produce(
                    CloudAnalyticsEventName.INFRA_SETUP_COMPLETE, succeeded=True,
                )
            except Exception as e:  # noqa: BLE001
                self.cloud_event_producer.produce(
                    CloudAnalyticsEventName.INFRA_SETUP_COMPLETE,
                    succeeded=False,
                    internal_error=str(e),
                )
                self.log.error(str(e))
                self.api_client.delete_cloud_api_v2_clouds_cloud_id_delete(
                    cloud_id=cloud_id
                )
                if deployment_succeed:
                    # only clean up deployment if it's created successfully
                    # otherwise keep the deployment for customers to check the errors
                    setup_utils.delete_gcp_deployment(
                        factory, project_id, deployment_name
                    )
                setup_utils.delete_workload_identity_pool(factory, pool_name, self.log)
                raise ClickException("Cloud setup failed!")

            self.log.info(f"Successfully created cloud {name}, and it's ready to use.")
        else:
            raise ClickException(
                f"Invalid Cloud provider: {provider}. Available providers are [aws, gcp]."
            )

        if len(functions_to_verify) > 0:
            CloudFunctionalVerificationController(
                self.cloud_event_producer, self.log
            ).start_verification(
                cloud_id,
                self._get_cloud_provider_from_str(provider),
                functions_to_verify,
                yes,
            )

    def _add_redis_cluster_aws(
        self, cloud: Any, cloud_resource: CreateCloudResource, yes: bool = False
    ):
        # Check if memorydb cluster already exists
        if cloud_resource.memorydb_cluster_config is not None:
            memorydb_name = cloud_resource.memorydb_cluster_config.id
            self.log.info(f"AWS memorydb {memorydb_name} already exists. ")
            return

        # Get or create memorydb cluster
        try:
            az_num = len(cloud_resource.aws_subnet_ids_with_availability_zones)
            memorydb_cluster_id = get_or_create_memorydb(
                cloud.region,
                cloud_resource.aws_cloudformation_stack_id,
                az_num,
                self.log,
                yes,
            )
            memorydb_cluster_config = _get_memorydb_cluster_config(
                memorydb_cluster_id, cloud.region, self.log
            )
        except Exception as e:  # noqa: BLE001
            raise ClickException(f"Cloud update failed! {e}")

        # Edit cloud resource record
        try:
            self.api_client.edit_cloud_resource_api_v2_clouds_with_cloud_resource_router_cloud_id_patch(
                cloud_id=cloud.id,
                editable_cloud_resource=EditableCloudResource(
                    memorydb_cluster_config=memorydb_cluster_config,
                ),
            )
        except Exception as e:  # noqa: BLE001
            self.log.error(str(e))
            raise ClickException(
                "Cloud update failed! Please reach out to Anyscale support or your SA for assistance."
            )

    def _add_redis_cluster_gcp(
        self, cloud: Any, cloud_resource: CreateCloudResourceGCP, yes: bool = False
    ):
        if cloud_resource.memorystore_instance_config is not None:
            memorystore_name = cloud_resource.memorystore_instance_config.name
            self.log.info(f"GCP memorystore {memorystore_name} already exists. ")
            return

        gcp_utils = try_import_gcp_utils()
        managed_setup_utils = try_import_gcp_managed_setup_utils()
        project_id = self._get_project_id(cloud, cloud.name, cloud.id)
        factory = gcp_utils.get_google_cloud_client_factory(self.log, project_id)
        deployment_name = cloud_resource.gcp_deployment_manager_id
        try:
            memorystore_instance_name = managed_setup_utils.get_or_create_memorystore_gcp(
                factory,
                cloud.id,
                deployment_name,
                project_id,
                cloud.region,
                self.log,
                yes,
            )
            memorystore_instance_config = gcp_utils.get_gcp_memorystore_config(
                factory, memorystore_instance_name
            )
        except Exception as e:  # noqa: BLE001
            raise ClickException(f"Failed to create GCP memorystore. Error: {e}")
        try:
            self.api_client.edit_cloud_resource_api_v2_clouds_with_cloud_resource_gcp_router_cloud_id_patch(
                cloud_id=cloud.id,
                editable_cloud_resource_gcp=EditableCloudResourceGCP(
                    memorystore_instance_config=memorystore_instance_config,
                ),
            )
        except Exception as e:  # noqa: BLE001
            self.log.error(str(e))
            raise ClickException(
                "Cloud update failed! Please reach out to Anyscale support or your SA for assistance."
            )

    def update_managed_cloud(  # noqa: PLR0912, C901
        self,
        cloud_name: Optional[str],
        cloud_id: Optional[str],
        enable_head_node_fault_tolerance: bool,
        functional_verify: Optional[str],
        yes: bool = False,
    ) -> None:
        """
        Updates managed cloud.

        If `enable_head_node_fault_tolerance` is set to True, we will add redis clusters to the cloud.
        Otherwise it only updates the inline IAM policies associated with the cross account IAM role for AWS clouds.
        """
        functions_to_verify = self._validate_functional_verification_args(
            functional_verify
        )
        cloud_id, cloud_name = get_cloud_id_and_name(
            self.api_client, cloud_id, cloud_name
        )
        cloud = self.api_client.get_cloud_api_v2_clouds_cloud_id_get(cloud_id).result
        if cloud.is_bring_your_own_resource or cloud.is_bring_your_own_resource is None:
            # If cloud.is_bring_your_own_resource is None, we couldn't tell it's a registered cloud or a managed cloud.
            # But it should be an old cloud so that we could just abort.
            raise ClickException(
                "Cannot update cloud with customer defined resources. Please modify the resources by `anyscale cloud edit`"
            )
        cloud_resource = get_cloud_resource_by_cloud_id(
            cloud_id, cloud.provider, self.api_client
        )
        if cloud_resource is None:
            raise ClickException(
                f"This cloud {cloud_name}({cloud_id}) does not contain resource records. Please delete this cloud and create a new one."
            )
        if enable_head_node_fault_tolerance:
            if cloud.provider == CloudProviders.AWS:
                self._add_redis_cluster_aws(cloud, cloud_resource, yes)
            elif cloud.provider == CloudProviders.GCP:
                self._add_redis_cluster_gcp(cloud, cloud_resource, yes)
            else:
                raise ClickException(
                    f"Unsupported cloud provider {cloud.provider}. Only AWS and GCP are supported for fault tolerance."
                )
        else:
            # Update IAM permissions
            if cloud.provider != CloudProviders.AWS:
                raise ClickException(
                    f"Unsupported cloud provider {cloud.provider}. Only AWS is supported for updating."
                )
            if anyscale_version == "0.0.0-dev":
                confirm(
                    "You are using a development version of Anyscale CLI. Still want to update the cloud?",
                    yes,
                )
            aws_cloudformation_stack_id = cloud_resource.aws_cloudformation_stack_id
            if aws_cloudformation_stack_id is None:
                raise ClickException(
                    f"This cloud {cloud.name}({cloud.id}) does not have an associated cloudformation stack. Please contact Anyscale support."
                )
            try:
                update_iam_role(
                    cloud.region, aws_cloudformation_stack_id, self.log, yes
                )
            except Exception as e:  # noqa: BLE001
                raise ClickException(f"Cloud update failed! {e}")
        self.log.info("Cloud update completed.")

        if len(functions_to_verify) > 0:
            CloudFunctionalVerificationController(
                self.cloud_event_producer, self.log
            ).start_verification(
                cloud_id, CloudProviders.AWS, functions_to_verify, yes,
            )

    def get_cloud_config(
        self, cloud_name: Optional[str] = None, cloud_id: Optional[str] = None,
    ) -> str:
        """Get a cloud's current JSON configuration."""

        cloud_id, cloud_name = get_cloud_id_and_name(
            self.api_client, cloud_id, cloud_name
        )

        return str(get_cloud_json_from_id(cloud_id, self.api_client)["config"])

    def set_default_cloud(
        self, cloud_name: Optional[str], cloud_id: Optional[str],
    ) -> None:
        """
        Sets default cloud for caller's organization. This operation can only be performed
        by organization admins, and the default cloud must have organization level
        permissions.
        """

        cloud_id, cloud_name = get_cloud_id_and_name(
            self.api_client, cloud_id, cloud_name
        )

        self.api_client.update_default_cloud_api_v2_organizations_update_default_cloud_post(
            cloud_id=cloud_id
        )

        self.log.info(f"Updated default cloud to {cloud_name}")

    def _passed_or_failed_str_from_bool(self, is_passing: bool) -> str:
        return "PASSED" if is_passing else "FAILED"

    @staticmethod
    def _get_cloud_provider_from_str(provider: str) -> CloudProviders:
        if provider.lower() == "aws":
            return CloudProviders.AWS
        elif provider.lower() == "gcp":
            return CloudProviders.GCP
        else:
            raise ClickException(
                f"Unsupported provider {provider}. Supported providers are [aws, gcp]."
            )

    def _validate_functional_verification_args(
        self, functional_verify: Optional[str]
    ) -> List[CloudFunctionalVerificationType]:
        if functional_verify is None:
            return []
        # validate functional_verify
        functions_to_verify = set()
        for function in functional_verify.split(","):
            fn = getattr(CloudFunctionalVerificationType, function.upper(), None)
            if fn is None:
                raise ClickException(
                    f"Unsupported function {function} for --functional-verify. "
                    f"Supported functions: {[function.lower() for function in CloudFunctionalVerificationType]}"
                )
            functions_to_verify.add(fn)
        return list(functions_to_verify)

    def verify_cloud(  # noqa: PLR0911
        self,
        *,
        cloud_name: Optional[str],
        cloud_id: Optional[str],
        functional_verify: Optional[str],
        boto3_session: Optional[Any] = None,
        strict: bool = False,
        _use_strict_iam_permissions: bool = False,  # This should only be used in testing.
        yes: bool = False,
    ) -> bool:
        """
        Verifies a cloud by name or id.

        Note: If your changes involve operations that may require additional permissions
        (for example, `boto3_session.client("efs").describe_backup_policy`), it's important
        to run the end-to-end test `bk_e2e/test_cloud.py` locally before pushing the changes.
        This way, you can ensure that your changes will not break the tests.
        """
        functions_to_verify = self._validate_functional_verification_args(
            functional_verify
        )

        cloud_id, cloud_name = get_cloud_id_and_name(
            self.api_client, cloud_id, cloud_name
        )

        cloud = self.api_client.get_cloud_api_v2_clouds_cloud_id_get(cloud_id).result

        if cloud.state == CloudState.DELETING or cloud.state == CloudState.DELETED:
            self.log.info(
                f"This cloud {cloud_name}({cloud_id}) is either during deletion or deleted. Skipping verification."
            )
            return False

        cloud_resource = get_cloud_resource_by_cloud_id(
            cloud_id, cloud.provider, self.api_client
        )
        if cloud_resource is None:
            self.log.error(
                f"This cloud {cloud_name}({cloud_id}) does not contain resource records. Please delete this cloud and create a new one."
            )
            return False

        self.cloud_event_producer.init_trace_context(
            CloudAnalyticsEventCommandName.VERIFY,
            cloud_provider=cloud.provider,
            cloud_id=cloud_id,
        )
        self.cloud_event_producer.produce(
            CloudAnalyticsEventName.COMMAND_START, succeeded=True
        )

        if cloud.provider == "AWS":
            if boto3_session is None:
                boto3_session = boto3.Session(region_name=cloud.region)
            if not self.verify_aws_cloud_resources(
                cloud_resource=cloud_resource,
                boto3_session=boto3_session,
                region=cloud.region,
                cloud_id=cloud_id,
                is_bring_your_own_resource=cloud.is_bring_your_own_resource,
                is_private_network=cloud.is_private_cloud
                if cloud.is_private_cloud
                else False,
                strict=strict,
                _use_strict_iam_permissions=_use_strict_iam_permissions,
            ):
                self.cloud_event_producer.produce(
                    CloudAnalyticsEventName.RESOURCES_VERIFIED,
                    succeeded=False,
                    logger=self.log,
                )
                return False
        elif cloud.provider == "GCP":
            project_id = json.loads(cloud.credentials)["project_id"]
            if not self.verify_gcp_cloud_resources(
                cloud_resource=cloud_resource,
                project_id=project_id,
                region=cloud.region,
                cloud_id=cloud_id,
                yes=False,
                strict=strict,
                is_private_service_cloud=cloud.is_private_service_cloud,
            ):
                self.cloud_event_producer.produce(
                    CloudAnalyticsEventName.RESOURCES_VERIFIED,
                    succeeded=False,
                    logger=self.log,
                )
                return False
        else:
            self.log.error(
                f"This cloud {cloud_name}({cloud_id}) does not have a valid cloud provider."
            )
            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.RESOURCES_VERIFIED,
                succeeded=False,
                internal_error="invalid cloud provider",
            )
            return False

        self.cloud_event_producer.produce(
            CloudAnalyticsEventName.RESOURCES_VERIFIED, succeeded=True
        )

        if len(functions_to_verify) == 0:
            return True

        return CloudFunctionalVerificationController(
            self.cloud_event_producer, self.log
        ).start_verification(cloud_id, cloud.provider, functions_to_verify, yes=yes)

    def verify_aws_cloud_resources(
        self,
        *,
        cloud_resource: CreateCloudResource,
        boto3_session: boto3.Session,
        region: str,
        is_private_network: bool,
        cloud_id: str,
        is_bring_your_own_resource: bool = False,
        ignore_capacity_errors: bool = IGNORE_CAPACITY_ERRORS,
        logger: CloudSetupLogger = None,
        strict: bool = False,
        _use_strict_iam_permissions: bool = False,  # This should only be used in testing.
    ):
        if not logger:
            logger = self.log

        verify_aws_vpc_result = verify_aws_vpc(
            cloud_resource=cloud_resource,
            boto3_session=boto3_session,
            logger=logger,
            ignore_capacity_errors=ignore_capacity_errors,
            strict=strict,
        )
        verify_aws_subnets_result = verify_aws_subnets(
            cloud_resource=cloud_resource,
            region=region,
            logger=logger,
            ignore_capacity_errors=ignore_capacity_errors,
            is_private_network=is_private_network,
            strict=strict,
        )

        anyscale_aws_account = (
            self.api_client.get_anyscale_aws_account_api_v2_clouds_anyscale_aws_account_get().result.anyscale_aws_account
        )
        verify_aws_iam_roles_result = verify_aws_iam_roles(
            cloud_resource=cloud_resource,
            boto3_session=boto3_session,
            anyscale_aws_account=anyscale_aws_account,
            logger=logger,
            strict=strict,
            cloud_id=cloud_id,
            _use_strict_iam_permissions=_use_strict_iam_permissions,
        )
        verify_aws_security_groups_result = verify_aws_security_groups(
            cloud_resource=cloud_resource,
            boto3_session=boto3_session,
            logger=logger,
            strict=strict,
        )
        verify_aws_s3_result = verify_aws_s3(
            cloud_resource=cloud_resource,
            boto3_session=boto3_session,
            region=region,
            logger=logger,
            strict=strict,
        )
        verify_aws_efs_result = verify_aws_efs(
            cloud_resource=cloud_resource,
            boto3_session=boto3_session,
            logger=logger,
            strict=strict,
        )
        # Cloudformation is only used in managed cloud setup. Set to True in BYOR case because it's not used.
        verify_aws_cloudformation_stack_result = True
        if not is_bring_your_own_resource:
            verify_aws_cloudformation_stack_result = verify_aws_cloudformation_stack(
                cloud_resource=cloud_resource,
                boto3_session=boto3_session,
                logger=logger,
                strict=strict,
            )
        if cloud_resource.memorydb_cluster_config is not None:
            verify_aws_memorydb_cluster_result = verify_aws_memorydb_cluster(
                cloud_resource=cloud_resource,
                boto3_session=boto3_session,
                logger=logger,
                strict=strict,
            )

        verify_anyscale_access_result = verify_anyscale_access(
            self.api_client, cloud_id, CloudProviders.AWS, logger
        )

        verification_result_summary = [
            "Verification result:",
            f"anyscale access: {self._passed_or_failed_str_from_bool(verify_anyscale_access_result)}",
            f"vpc: {self._passed_or_failed_str_from_bool(verify_aws_vpc_result)}",
            f"subnets: {self._passed_or_failed_str_from_bool(verify_aws_subnets_result)}",
            f"iam roles: {self._passed_or_failed_str_from_bool(verify_aws_iam_roles_result)}",
            f"security groups: {self._passed_or_failed_str_from_bool(verify_aws_security_groups_result)}",
            f"s3: {self._passed_or_failed_str_from_bool(verify_aws_s3_result)}",
            f"efs: {self._passed_or_failed_str_from_bool(verify_aws_efs_result)}",
            f"cloudformation stack: {self._passed_or_failed_str_from_bool(verify_aws_cloudformation_stack_result) if not is_bring_your_own_resource else 'N/A'}",
        ]
        if cloud_resource.memorydb_cluster_config is not None:
            verification_result_summary.append(
                f"memorydb cluster: {self._passed_or_failed_str_from_bool(verify_aws_memorydb_cluster_result)}"
            )

        logger.info("\n".join(verification_result_summary))

        return all(
            [
                verify_anyscale_access_result,
                verify_aws_vpc_result,
                verify_aws_subnets_result,
                verify_aws_iam_roles_result,
                verify_aws_security_groups_result,
                verify_aws_s3_result,
                verify_aws_efs_result,
                verify_aws_cloudformation_stack_result
                if not is_bring_your_own_resource
                else True,
            ]
        )

    def register_aws_cloud(  # noqa: PLR0913, PLR0912
        self,
        *,
        region: str,
        name: str,
        vpc_id: str,
        subnet_ids: List[str],
        efs_id: str,
        anyscale_iam_role_id: str,
        instance_iam_role_id: str,
        security_group_ids: List[str],
        s3_bucket_id: str,
        memorydb_cluster_id: Optional[str],
        functional_verify: Optional[str],
        private_network: bool,
        cluster_management_stack_version: ClusterManagementStackVersions,
        yes: bool = False,
    ):
        functions_to_verify = self._validate_functional_verification_args(
            functional_verify
        )
        self.cloud_event_producer.init_trace_context(
            CloudAnalyticsEventCommandName.REGISTER, CloudProviders.AWS
        )
        self.cloud_event_producer.produce(
            CloudAnalyticsEventName.COMMAND_START, succeeded=True
        )

        # Create a cloud without cloud resources first
        try:
            created_cloud = self.api_client.create_cloud_api_v2_clouds_post(
                write_cloud=WriteCloud(
                    provider="AWS",
                    region=region,
                    credentials=anyscale_iam_role_id,
                    name=name,
                    is_bring_your_own_resource=True,
                    is_private_cloud=private_network,
                    cluster_management_stack_version=cluster_management_stack_version,
                )
            )
            cloud_id = created_cloud.result.id
            self.cloud_event_producer.set_cloud_id(cloud_id)
            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.CLOUD_RECORD_INSERTED, succeeded=True
            )
        except ClickException as e:
            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.CLOUD_RECORD_INSERTED,
                succeeded=False,
                internal_error=str(e),
            )
            if "409" in e.message:
                raise ClickException(
                    f"Cloud with name {name} already exists. Please choose a different name."
                )
            raise

        try:
            # Update anyscale IAM role's assume policy to include the cloud id as the external ID
            role = _get_role(
                AwsRoleArn.from_string(anyscale_iam_role_id).to_role_name(), region
            )
            if role is None:
                self.log.log_resource_error(
                    CloudAnalyticsEventCloudResource.AWS_IAM_ROLE,
                    CloudSetupError.RESOURCE_NOT_FOUND,
                )
                raise ClickException(
                    f"Failed to access IAM role {anyscale_iam_role_id}."
                )
            try:
                new_policy = _update_external_ids_for_policy(
                    role.assume_role_policy_document, cloud_id  # type: ignore
                )
                role.AssumeRolePolicy().update(PolicyDocument=json.dumps(new_policy))  # type: ignore
            except ClientError as e:
                self.log.log_resource_exception(
                    CloudAnalyticsEventCloudResource.AWS_IAM_ROLE, e
                )
                raise e

            try:
                boto3_session = boto3.Session(region_name=region)
                aws_efs_mount_target_ip = _get_aws_efs_mount_target_ip(
                    boto3_session, efs_id, self.log
                )
            except ClientError as e:
                raise e

            aws_subnet_ids_with_availability_zones = associate_aws_subnets_with_azs(
                subnet_ids, region, self.log
            )

            if memorydb_cluster_id is not None:
                memorydb_cluster_config = _get_memorydb_cluster_config(
                    memorydb_cluster_id, region, self.log
                )
            else:
                memorydb_cluster_config = None

            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.PREPROCESS_COMPLETE, succeeded=True
            )
        except Exception as e:  # noqa: BLE001
            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.PREPROCESS_COMPLETE,
                succeeded=False,
                logger=self.log,
            )
            # Delete the cloud if registering the cloud fails
            self.api_client.delete_cloud_api_v2_clouds_cloud_id_delete(
                cloud_id=cloud_id
            )
            # If it is a credentials error, rewrite the error to be more clear
            if isinstance(e, NoCredentialsError):
                raise ClickException(
                    "Unable to locate AWS credentials. Cloud registration requires valid AWS credentials to be set locally. Learn more: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html"
                )
            raise ClickException(f"Cloud registration failed! {e}")

        try:
            # Verify cloud resources meet our requirement
            create_cloud_resource = CreateCloudResource(
                aws_vpc_id=vpc_id,
                aws_subnet_ids_with_availability_zones=aws_subnet_ids_with_availability_zones,
                aws_iam_role_arns=[anyscale_iam_role_id, instance_iam_role_id],
                aws_security_groups=security_group_ids,
                aws_s3_id=s3_bucket_id,
                aws_efs_id=efs_id,
                aws_efs_mount_target_ip=aws_efs_mount_target_ip,
                memorydb_cluster_config=memorydb_cluster_config,
            )
            with self.log.spinner("Verifying cloud resources...") as spinner:
                if not self.verify_aws_cloud_resources(
                    cloud_resource=create_cloud_resource,
                    boto3_session=boto3_session,
                    region=region,
                    is_bring_your_own_resource=True,
                    is_private_network=private_network,
                    cloud_id=cloud_id,
                    logger=CloudSetupLogger(spinner_manager=spinner),
                ):
                    raise ClickException(
                        "Please make sure all the resources provided meet the requirements and try again."
                    )

            confirm(
                "Please review the output from verification for any warnings. Would you like to proceed with cloud creation?",
                yes,
            )
            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.RESOURCES_VERIFIED, succeeded=True
            )
        except Exception as e:  # noqa: BLE001
            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.RESOURCES_VERIFIED,
                succeeded=False,
                logger=self.log,
            )
            # Delete the cloud if registering the cloud fails
            self.api_client.delete_cloud_api_v2_clouds_cloud_id_delete(
                cloud_id=cloud_id
            )

            raise ClickException(f"Cloud registration failed! {e}")

        try:
            with self.log.spinner(
                "Updating Anyscale cloud with cloud resource..."
            ) as spinner:
                # update cloud with verified cloud resources
                self.api_client.update_cloud_with_cloud_resource_api_v2_clouds_with_cloud_resource_router_cloud_id_put(
                    cloud_id=cloud_id,
                    update_cloud_with_cloud_resource=UpdateCloudWithCloudResource(
                        cloud_resource_to_update=create_cloud_resource,
                    ),
                )
            self.wait_for_cloud_to_be_active(cloud_id)
            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.INFRA_SETUP_COMPLETE, succeeded=True
            )
        except Exception as e:  # noqa: BLE001
            # Delete the cloud if registering the cloud fails
            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.INFRA_SETUP_COMPLETE,
                succeeded=False,
                internal_error=str(e),
            )
            self.api_client.delete_cloud_api_v2_clouds_cloud_id_delete(
                cloud_id=cloud_id
            )

            raise ClickException(f"Cloud registration failed! {e}")

        self.log.info(
            f"Successfully created cloud {name}, id: {cloud_id}, and it's ready to use."
        )

        if len(functions_to_verify) > 0:
            CloudFunctionalVerificationController(
                self.cloud_event_producer, self.log
            ).start_verification(cloud_id, CloudProviders.AWS, functions_to_verify, yes)

    def verify_gcp_cloud_resources(
        self,
        *,
        cloud_resource: CreateCloudResourceGCP,
        project_id: str,
        region: str,
        cloud_id: str,
        yes: bool,
        factory: Any = None,
        strict: bool = False,
        is_private_service_cloud: bool = False,
    ) -> bool:
        gcp_utils = try_import_gcp_utils()
        if not factory:
            factory = gcp_utils.get_google_cloud_client_factory(self.log, project_id)
        GCPLogger = gcp_utils.GCPLogger
        verify_lib = try_import_gcp_verify_lib()

        with self.log.spinner("Verifying cloud resources...") as spinner:
            gcp_logger = GCPLogger(self.log, project_id, spinner, yes)
            verify_gcp_project_result = verify_lib.verify_gcp_project(
                factory, cloud_resource, project_id, gcp_logger, strict=strict
            )
            verify_gcp_access_service_account_result = verify_lib.verify_gcp_access_service_account(
                factory, cloud_resource, project_id, gcp_logger
            )
            verify_gcp_dataplane_service_account_result = verify_lib.verify_gcp_dataplane_service_account(
                factory, cloud_resource, project_id, gcp_logger, strict=strict
            )
            verify_gcp_networking_result = verify_lib.verify_gcp_networking(
                factory,
                cloud_resource,
                project_id,
                region,
                gcp_logger,
                strict=strict,
                is_private_service_cloud=is_private_service_cloud,
            )
            verify_firewall_policy_result = verify_lib.verify_firewall_policy(
                factory, cloud_resource, project_id, region, gcp_logger, strict=strict,
            )
            verify_filestore_result = verify_lib.verify_filestore(
                factory, cloud_resource, region, gcp_logger, strict=strict
            )
            verify_cloud_storage_result = verify_lib.verify_cloud_storage(
                factory, cloud_resource, project_id, region, gcp_logger, strict=strict,
            )
            verify_anyscale_access_result = verify_anyscale_access(
                self.api_client, cloud_id, CloudProviders.GCP, self.log
            )
            verify_memorystore_result = True
            if cloud_resource.memorystore_instance_config is not None:
                verify_memorystore_result = verify_lib.verify_memorystore(
                    factory, cloud_resource, gcp_logger, strict=strict,
                )

        verification_results = [
            "Verification result:",
            f"anyscale access: {self._passed_or_failed_str_from_bool(verify_anyscale_access_result)}",
            f"project: {self._passed_or_failed_str_from_bool(verify_gcp_project_result)}",
            f"vpc and subnet: {self._passed_or_failed_str_from_bool(verify_gcp_networking_result)}",
            f"anyscale iam service account: {self._passed_or_failed_str_from_bool(verify_gcp_access_service_account_result)}",
            f"cluster node service account: {self._passed_or_failed_str_from_bool(verify_gcp_dataplane_service_account_result)}",
            f"firewall policy: {self._passed_or_failed_str_from_bool(verify_firewall_policy_result)}",
            f"filestore: {self._passed_or_failed_str_from_bool(verify_filestore_result)}",
            f"cloud storage: {self._passed_or_failed_str_from_bool(verify_cloud_storage_result)}",
        ]

        if cloud_resource.memorystore_instance_config is not None:
            verification_results.append(
                f"memorystore: {self._passed_or_failed_str_from_bool(verify_memorystore_result)}"
            )

        self.log.info("\n".join(verification_results))

        return all(
            [
                verify_anyscale_access_result,
                verify_gcp_project_result,
                verify_gcp_access_service_account_result,
                verify_gcp_dataplane_service_account_result,
                verify_gcp_networking_result,
                verify_firewall_policy_result,
                verify_filestore_result,
                verify_cloud_storage_result,
                verify_memorystore_result,
            ]
        )

    def register_gcp_cloud(  # noqa: PLR0913
        self,
        *,
        region: str,
        name: str,
        project_id: str,
        vpc_name: str,
        subnet_names: List[str],
        filestore_instance_id: str,
        filestore_location: str,
        anyscale_service_account_email: str,
        instance_service_account_email: str,
        provider_id: str,
        firewall_policy_names: List[str],
        cloud_storage_bucket_name: str,
        memorystore_instance_name: Optional[str],
        functional_verify: Optional[str],
        private_network: bool,
        cluster_management_stack_version: ClusterManagementStackVersions,
        yes: bool = False,
    ):
        functions_to_verify = self._validate_functional_verification_args(
            functional_verify
        )
        gcp_utils = try_import_gcp_utils()

        # Create a cloud without cloud resources first
        assert re.search(
            "projects/[0-9]*/locations/global/workloadIdentityPools/.+/providers/.+",
            provider_id,
        ), f"Invalid provider_id {provider_id}"

        self.cloud_event_producer.init_trace_context(
            CloudAnalyticsEventCommandName.REGISTER, CloudProviders.GCP
        )
        self.cloud_event_producer.produce(
            CloudAnalyticsEventName.COMMAND_START, succeeded=True
        )

        try:
            credentials = json.dumps(
                {
                    "project_id": project_id,
                    "provider_id": provider_id,
                    "service_account_email": anyscale_service_account_email,
                }
            )

            created_cloud = self.api_client.create_cloud_api_v2_clouds_post(
                write_cloud=WriteCloud(
                    provider="GCP",
                    region=region,
                    credentials=credentials,
                    name=name,
                    is_bring_your_own_resource=True,
                    is_private_cloud=private_network,
                    cluster_management_stack_version=cluster_management_stack_version,
                )
            )
            cloud_id = created_cloud.result.id
            self.cloud_event_producer.set_cloud_id(cloud_id)
            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.CLOUD_RECORD_INSERTED, succeeded=True
            )
        except ClickException as e:
            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.CLOUD_RECORD_INSERTED,
                succeeded=False,
                internal_error=str(e),
            )
            if "409" in e.message:
                raise ClickException(
                    f"Cloud with name {name} already exists. Please choose a different name."
                )
            raise

        try:
            factory = gcp_utils.get_google_cloud_client_factory(self.log, project_id)

            filestore_config = gcp_utils.get_gcp_filestore_config(
                factory,
                project_id,
                vpc_name,
                filestore_location,
                filestore_instance_id,
                self.log,
            )

            memorystore_instance_config = gcp_utils.get_gcp_memorystore_config(
                factory, memorystore_instance_name
            )

            # Verify cloud resources meet our requirement
            create_cloud_resource_gcp = CreateCloudResourceGCP(
                gcp_vpc_id=vpc_name,
                gcp_subnet_ids=subnet_names,
                gcp_cluster_node_service_account_email=instance_service_account_email,
                gcp_anyscale_iam_service_account_email=anyscale_service_account_email,
                gcp_filestore_config=filestore_config,
                gcp_firewall_policy_ids=firewall_policy_names,
                gcp_cloud_storage_bucket_id=cloud_storage_bucket_name,
                memorystore_instance_config=memorystore_instance_config,
            )

            if not self.verify_gcp_cloud_resources(
                cloud_resource=create_cloud_resource_gcp,
                project_id=project_id,
                region=region,
                cloud_id=cloud_id,
                yes=yes,
                factory=factory,
            ):
                raise ClickException(
                    "Please make sure all the resources provided meet the requirements and try again."
                )

            confirm(
                "Please review the output from verification for any warnings. Would you like to proceed with cloud creation?",
                yes,
            )
            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.RESOURCES_VERIFIED, succeeded=True
            )
        except Exception as e:  # noqa: BLE001
            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.RESOURCES_VERIFIED,
                succeeded=False,
                logger=self.log,
            )

            # Delete the cloud if registering the cloud fails
            self.api_client.delete_cloud_api_v2_clouds_cloud_id_delete(
                cloud_id=cloud_id
            )
            raise ClickException(f"Cloud registration failed! {e}")

        try:
            # update cloud with verified cloud resources
            with self.log.spinner("Updating Anyscale cloud with cloud resources..."):
                self.api_client.update_cloud_with_cloud_resource_api_v2_clouds_with_cloud_resource_gcp_router_cloud_id_put(
                    cloud_id=cloud_id,
                    update_cloud_with_cloud_resource_gcp=UpdateCloudWithCloudResourceGCP(
                        cloud_resource_to_update=create_cloud_resource_gcp,
                    ),
                )
            self.wait_for_cloud_to_be_active(cloud_id)
            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.INFRA_SETUP_COMPLETE, succeeded=True
            )
        except Exception as e:  # noqa: BLE001
            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.INFRA_SETUP_COMPLETE,
                succeeded=False,
                internal_error=str(e),
            )
            # Delete the cloud if registering the cloud fails
            self.api_client.delete_cloud_api_v2_clouds_cloud_id_delete(
                cloud_id=cloud_id
            )
            raise ClickException(f"Cloud registration failed! {e}")

        self.log.info(
            f"Successfully created cloud {name}, id: {cloud_id}, and it's ready to use."
        )

        if len(functions_to_verify) > 0:
            CloudFunctionalVerificationController(
                self.cloud_event_producer, self.log
            ).start_verification(cloud_id, CloudProviders.GCP, functions_to_verify, yes)

    def delete_cloud(  # noqa: PLR0912
        self,
        cloud_name: Optional[str],
        cloud_id: Optional[str],
        skip_confirmation: bool,
    ) -> bool:
        """
        Deletes a cloud by name or id.
        TODO Delete all GCE resources on cloud delete
        Including: Anyscale maanged resources, ALB resources, and TLS certs
        """
        cloud_id, cloud_name = get_cloud_id_and_name(
            self.api_client, cloud_id, cloud_name
        )

        # get cloud
        cloud = self.api_client.get_cloud_api_v2_clouds_cloud_id_get(
            cloud_id=cloud_id
        ).result

        cloud_provider = cloud.provider
        assert cloud_provider in (
            CloudProviders.AWS,
            CloudProviders.GCP,
        ), f"Cloud provider {cloud_provider} not supported yet"

        cloud_resource = get_cloud_resource_by_cloud_id(
            cloud_id, cloud.provider, self.api_client
        )
        if cloud_resource is None:
            # no cloud resource found, directly delete the cloud
            try:
                self.api_client.delete_cloud_api_v2_clouds_cloud_id_delete(
                    cloud_id=cloud_id
                )
            except ClickException as e:
                self.log.error(e)
                raise ClickException(f"Failed to delete cloud with name {cloud_name}.")

            self.log.info(f"Deleted cloud with name {cloud_name}.")
            return True

        confirmation_msg = f"\nIf the cloud {cloud_id} is deleted, you will not be able to access existing clusters of this cloud.\n"
        if cloud.is_bring_your_own_resource:
            confirmation_msg += "Note that Anyscale does not delete any of the cloud provider resources created by you.\n"

        confirm(
            f"{confirmation_msg}\nFor more information, please refer to the documentation https://docs.anyscale.com/cloud-deployment/{cloud_provider.lower()}/manage-clouds#delete-an-anyscale-cloud\nContinue?",
            skip_confirmation,
        )

        # set cloud state to DELETING
        try:
            if cloud_provider == CloudProviders.AWS:
                with self.log.spinner("Deleting Anyscale cloud..."):
                    response = self.api_client.update_cloud_with_cloud_resource_api_v2_clouds_with_cloud_resource_router_cloud_id_put(
                        cloud_id=cloud_id,
                        update_cloud_with_cloud_resource=UpdateCloudWithCloudResource(
                            state=CloudState.DELETING
                        ),
                    )
            elif cloud_provider == CloudProviders.GCP:
                with self.log.spinner("Deleting Anyscale cloud..."):
                    response = self.api_client.update_cloud_with_cloud_resource_api_v2_clouds_with_cloud_resource_gcp_router_cloud_id_put(
                        cloud_id=cloud_id,
                        update_cloud_with_cloud_resource_gcp=UpdateCloudWithCloudResourceGCP(
                            state=CloudState.DELETING
                        ),
                    )
            cloud = response.result
        except ClickException as e:
            self.log.error(e)
            raise ClickException(
                f"Failed to update cloud state to deleting for cloud {cloud_name}."
            )

        if cloud.is_bring_your_own_resource is False:
            # managed setup clouds
            if cloud_provider == CloudProviders.AWS:
                self.delete_all_aws_resources(cloud, skip_confirmation)

            elif cloud_provider == CloudProviders.GCP:
                try:
                    self.delete_gcp_managed_cloud(cloud=cloud)
                except ClickException as e:
                    confirm(
                        f"Error while trying to clean up {cloud_provider} resources:\n{e}\n"
                        "Do you want to force delete this cloud? You will need to clean up any associated resources on your own.\n"
                        "Continue with force deletion?",
                        skip_confirmation,
                    )
        elif (
            cloud_provider == CloudProviders.AWS
            and not cloud.is_k8s
            and not cloud.is_aioa
        ):
            # AWS registerted cloud
            self.log.warning(
                f"The trust policy that allows Anyscale to assume {cloud.credentials} is still in place. Please delete it manually if you no longer wish anyscale to have access."
            )
            self.log.warning(
                "If services v2 were used in this cloud, please delete all TLS certificates and ALB stacks associated to the cloud to avoid unintended costs on your AWS account. "
            )
        elif (
            cloud_provider == CloudProviders.GCP
            and not cloud.is_k8s
            and not cloud.is_aioa
        ):
            # GCP registered cloud
            credentials = json.loads(cloud.credentials)
            provider = credentials["gcp_workload_identity_pool_id"]
            service_account = credentials["service_account_email"]
            self.log.warning(
                f"The workload identity federation provider pool {provider} and service account {service_account} that allows Anyscale to access your GCP account is still in place. Please delete it manually if you no longer wish anyscale to have access."
            )
        try:
            self.api_client.delete_cloud_api_v2_clouds_cloud_id_delete(
                cloud_id=cloud_id
            )
        except ClickException as e:
            self.log.error(e)
            raise ClickException(f"Failed to delete cloud with name {cloud_name}.")

        self.log.info(f"Deleted cloud with name {cloud_name}.")
        return True

    def delete_all_aws_resources(
        self, cloud: CloudWithCloudResource, skip_confirmation: bool
    ) -> bool:
        # Delete service v2 resources
        # If there is an error while cleaning up service v2 resources, abort
        try:
            self.delete_tagged_managed_resources(cloud=cloud)
            self.delete_tls_certs(cloud=cloud)
        except ClickException as e:
            raise ClickException(
                f"Error while trying to cleanup service v2 resources:\n{e}\n"
                "Please check your AWS account for relevant errors. "
                "Manually delete the aforementioned resources and rerun cloud delete once resolved. "
                "If you experience issues, reach out to Anyscale support for help."
            )
        try:
            # If the cloud is updated, the cross account IAM role might have an inline policy for customer drifts
            # We delete the inline policy first otherwise cfn stack deletion would fail
            try_delete_customer_drifts_policy(cloud=cloud)
            # Delete AWS cloud resources by deleting the cfn stack
            self.delete_aws_managed_cloud(cloud=cloud)
        except ClickException as e:
            confirm(
                f"Error while trying to clean up cloud resources:\n{e}\n"
                "Do you want to force delete this cloud? You will need to clean up any associated resources on your own.\n"
                "Continue with force deletion?",
                skip_confirmation,
            )

        return True

    def delete_tls_certs(self, cloud: CloudWithCloudResource) -> bool:
        tag_name = "anyscale-cloud-id"
        key_name = cloud.id

        acm = boto3.client("acm", cloud.region)

        response = acm.list_certificates()

        matching_certs = []

        if "CertificateSummaryList" in response:
            for certificate in response["CertificateSummaryList"]:
                if "CertificateArn" in certificate:

                    certificate_arn = certificate["CertificateArn"]
                    response = acm.list_tags_for_certificate(
                        CertificateArn=certificate_arn
                    )

                    if "Tags" in response:
                        tags = response["Tags"]
                        for tag in tags:
                            if (
                                "Key" in tag
                                and tag["Key"] == tag_name
                                and "Value" in tag
                                and tag["Value"] == key_name
                            ):
                                matching_certs.append(certificate_arn)

        resource_delete_status = []
        for certificate_arn in matching_certs:
            resource_delete_status.append(self.delete_tls_cert(certificate_arn, cloud))
        return all(resource_delete_status)

    def delete_aws_managed_cloud(self, cloud: CloudWithCloudResource) -> bool:
        if (
            not cloud.cloud_resource
            or not cloud.cloud_resource.aws_cloudformation_stack_id
        ):
            raise ClickException(
                f"This cloud {cloud.id} does not have a cloudformation stack."
            )

        cfn_stack_arn = cloud.cloud_resource.aws_cloudformation_stack_id

        self.log.info(
            f"\nThe S3 bucket ({cloud.cloud_resource.aws_s3_id}) associated with this cloud still exists."
            "\nIf you no longer need the data associated with this bucket, please delete it."
        )

        return self.delete_aws_cloudformation_stack(
            cfn_stack_arn=cfn_stack_arn, cloud=cloud
        )

    def delete_tagged_managed_resources(self, cloud: CloudWithCloudResource) -> bool:

        tag_name = "anyscale-cloud-id"
        key_name = cloud.id

        cfn_client = _client("cloudformation", cloud.region)
        # Get a list of all the CloudFormation stacks with the specified tag
        stacks = cfn_client.list_stacks()

        resources_to_cleanup = []

        for stack in stacks.get("StackSummaries", []):
            if "StackName" in stack and "StackId" in stack:
                cfn_stack_arn = stack["StackId"]
                stack["StackName"]

                stack_description = cfn_client.describe_stacks(StackName=cfn_stack_arn)

                # Extract the tags from the response
                if (
                    "Stacks" in stack_description
                    and stack_description["Stacks"]
                    and "Tags" in stack_description["Stacks"][0]
                ):
                    tags = stack_description["Stacks"][0]["Tags"]
                    for tag in tags:
                        if (
                            "Key" in tag
                            and tag["Key"] == tag_name
                            and "Value" in tag
                            and tag["Value"] == key_name
                        ):
                            resources_to_cleanup.append(cfn_stack_arn)

        resource_delete_status = []
        for cfn_stack_arn in resources_to_cleanup:
            resource_delete_status.append(
                self.delete_aws_cloudformation_stack(
                    cfn_stack_arn=cfn_stack_arn, cloud=cloud
                )
            )

        return all(resource_delete_status)

    def delete_aws_cloudformation_stack(
        self, cfn_stack_arn: str, cloud: CloudWithCloudResource
    ) -> bool:
        cfn_client = _client("cloudformation", cloud.region)

        cfn_stack_url = f"https://{cloud.region}.console.aws.amazon.com/cloudformation/home?region={cloud.region}#/stacks/stackinfo?stackId={cfn_stack_arn}"

        try:
            cfn_client.delete_stack(StackName=cfn_stack_arn)
        except ClientError:
            raise ClickException(
                f"Failed to delete cloudformation stack {cfn_stack_arn}.\nPlease view it at {cfn_stack_url}"
            ) from None

        self.log.info(f"\nTrack progress of cloudformation at {cfn_stack_url}")
        with self.log.spinner(
            f"Deleting cloud resource {cfn_stack_arn} through cloudformation..."
        ):
            end_time = time.time() + CLOUDFORMATION_TIMEOUT_SECONDS_LONG
            while time.time() < end_time:
                try:
                    cfn_stack = cfn_client.describe_stacks(StackName=cfn_stack_arn)[
                        "Stacks"
                    ][0]
                except ClientError as e:
                    raise ClickException(
                        f"Failed to fetch the cloudformation stack {cfn_stack_arn}. Please check you have the right AWS credentials and the cloudformation stack still exists. Error details: {e}"
                    ) from None

                if cfn_stack["StackStatus"] == "DELETE_COMPLETE":
                    self.log.info(
                        f"Cloudformation stack {cfn_stack['StackId']} is deleted."
                    )
                    break

                if cfn_stack["StackStatus"] in ("DELETE_FAILED"):
                    # Provide link to cloudformation
                    raise ClickException(
                        f"Failed to delete cloud resources. Please check your cloudformation stack for errors. {cfn_stack_url}"
                    )
                time.sleep(1)

            if time.time() > end_time:
                raise ClickException(
                    f"Timed out deleting AWS resources. Please check your cloudformation stack for errors. {cfn_stack['StackId']}"
                )

        return True

    def delete_tls_cert(
        self, certificate_arn: str, cloud: CloudWithCloudResource
    ) -> bool:
        acm = boto3.client("acm", cloud.region)

        try:
            acm.delete_certificate(CertificateArn=certificate_arn)
        except ClientError as e:
            raise ClickException(
                f"Failed to delete TLS certificate {certificate_arn}: {e}"
            ) from None

        return True

    def delete_gcp_managed_cloud(self, cloud: CloudWithCloudResourceGCP) -> bool:
        if (
            not cloud.cloud_resource
            or not cloud.cloud_resource.gcp_deployment_manager_id
        ):
            raise ClickException(
                f"This cloud {cloud.id} does not have a deployment in GCP deployment manager."
            )
        setup_utils = try_import_gcp_managed_setup_utils()
        gcp_utils = try_import_gcp_utils()

        project_id = json.loads(cloud.credentials)["project_id"]
        factory = gcp_utils.get_google_cloud_client_factory(self.log, project_id)
        deployment_name = cloud.cloud_resource.gcp_deployment_manager_id
        deployment_url = f"https://console.cloud.google.com/dm/deployments/details/{deployment_name}?project={project_id}"

        self.log.info(f"\nTrack progress of Deployment Manager at {deployment_url}")

        with self.log.spinner("Deleting cloud resources through Deployment Manager..."):

            # Remove firewall policy ids
            if cloud.cloud_resource.gcp_firewall_policy_ids:
                for firewall_policy in cloud.cloud_resource.gcp_firewall_policy_ids:
                    # try delete the associations
                    setup_utils.remove_firewall_policy_associations(
                        factory, project_id, firewall_policy
                    )

            # Delete the deployment
            setup_utils.update_deployment_with_bucket_only(
                factory, project_id, deployment_name
            )

        self.log.info(
            f"\nThe cloud bucket ({cloud.cloud_resource.gcp_cloud_storage_bucket_id}) associated with this cloud still exists."
            "\nIf you no longer need the data associated with this bucket, please delete it."
        )
        return True

    ### Edit cloud ###
    def _get_cloud_resource_value(self, cloud_resource: Any, resource_type: str) -> Any:
        # Special case -- memorydb_cluster_id
        if resource_type == "memorydb_cluster_id":
            memorydb_cluster_config = getattr(
                cloud_resource, "memorydb_cluster_config", None
            )
            if memorydb_cluster_config is None:
                return None
            else:
                # memorydb_cluster_config.id has format "arn:aws:memorydb:us-east-2:815664363732:cluster/cloud-edit-test".
                value = memorydb_cluster_config.id.split("/")[-1]
                return value

        # Special case -- memorystore_instance_name
        if resource_type == "memorystore_instance_name":
            memorystore_instance_config = getattr(
                cloud_resource, "memorystore_instance_config", None
            )
            if memorystore_instance_config is None:
                return None
            else:
                value = memorystore_instance_config.name
                return value

        # Normal cases.
        value = getattr(cloud_resource, resource_type, None)
        if value is None:
            self.log.warning(f"Old value of {resource_type} is None.")
            return None
        return value

    def _generate_edit_details_logs(
        self, cloud_resource: Any, edit_details: Dict[str, Optional[str]]
    ) -> List[str]:
        details_logs = []
        for resource_type, value in edit_details.items():
            if value:
                old_value = self._get_cloud_resource_value(
                    cloud_resource, resource_type
                )
                if old_value == value:
                    raise ClickException(
                        f"Specified resource is the same as existed resource -- {resource_type}: {value}"
                    )
                details_logs.append(f"{resource_type}: from {old_value} -> {value}")
        return details_logs

    def _generate_rollback_command(
        self, cloud_id: str, cloud_resource: Any, edit_details: Dict[str, Optional[str]]
    ) -> str:
        rollback_command = BASE_ROLLBACK_COMMAND.format(cloud_id=cloud_id)
        for resource_type, value in edit_details.items():
            if value:
                old_value = self._get_cloud_resource_value(
                    cloud_resource, resource_type
                )
                if old_value is not None:
                    # The resource type names are in CreateCloudResource (backend/server/api/product/models/clouds.py).
                    # The cli command names are in cloud_edit (frontend/cli/anyscale/commands:cloud_commands).
                    # The relationship between their names are cli_command_name = resource_type_name.replace("_", "-").
                    # e.g. cli_command_name: aws-s3-id & resource_type_name: aws_s3_id.
                    formatted_resource_type = resource_type.replace("_", "-")
                    rollback_command += f" --{formatted_resource_type}={old_value}"
        # If the only edit field is redis and it was None originally, rollback_command didn't appened any args, reset the rollback command to be empty.
        if rollback_command == BASE_ROLLBACK_COMMAND.format(cloud_id=cloud_id):
            rollback_command = ""
        return rollback_command

    def _edit_aws_cloud(  # noqa: PLR0912
        self,
        *,
        cloud_id: str,
        cloud_name: str,
        cloud: Any,
        cloud_resource: Any,
        aws_s3_id: Optional[str],
        aws_efs_id: Optional[str],
        aws_efs_mount_target_ip: Optional[str],
        memorydb_cluster_id: Optional[str],
        yes: bool = False,
    ):
        # Log edit details.
        self.log.open_block("EditDetail", "\nEdit details...")
        edit_details = {
            "aws_s3_id": aws_s3_id,
            "aws_efs_id": aws_efs_id,
            "aws_efs_mount_target_ip": aws_efs_mount_target_ip,
            "memorydb_cluster_id": memorydb_cluster_id,
        }
        details_logs = self._generate_edit_details_logs(cloud_resource, edit_details)
        self.log.info(
            self.log.highlight(
                "Cloud {} ({}) edit details: \n{}".format(
                    cloud_name, cloud_id, "; \n".join(details_logs)
                )
            )
        )
        self.log.close_block("EditDetail")

        try:
            boto3_session = boto3.Session(region_name=cloud.region)
            if aws_efs_id and not aws_efs_mount_target_ip:
                # Get the mount target IP for new aws_efs_ip (consistent with cloud register).
                aws_efs_mount_target_ip = _get_aws_efs_mount_target_ip(
                    boto3_session, aws_efs_id, self.log
                )
                if not aws_efs_mount_target_ip:
                    raise ClickException(
                        f"Failed to get the mount target IP for new aws_efs_ip {aws_efs_id}, please make sure the aws_efs_ip exists and it has mount targets."
                    )
        except Exception as e:  # noqa: BLE001
            self.log.error(str(e))
            raise ClickException(
                f"Failed to get the mount target IP for new aws_efs_ip {aws_efs_id}, please make sure it has mount targets."
            )
        try:
            memorydb_cluster_config = None
            if memorydb_cluster_id:
                memorydb_cluster_config = _get_memorydb_cluster_config(
                    memorydb_cluster_id, cloud.region, self.log
                )
        except Exception as e:  # noqa: BLE001
            self.log.error(str(e))
            raise ClickException(
                f"Failed to get the memorydb cluster config for new memorydb_cluster_id {memorydb_cluster_id}, please make sure it's created."
            )

        # Static Verify.
        self.log.open_block(
            "Verify", "Start cloud static verification on the specified resources..."
        )
        new_cloud_resource = copy.deepcopy(cloud_resource)
        if aws_s3_id:
            new_cloud_resource.aws_s3_id = aws_s3_id
        if aws_efs_id:
            new_cloud_resource.aws_efs_id = aws_efs_id
        if aws_efs_mount_target_ip:
            new_cloud_resource.aws_efs_mount_target_ip = aws_efs_mount_target_ip
        if memorydb_cluster_id:
            new_cloud_resource.memorydb_cluster_config = memorydb_cluster_config

        if not self.verify_aws_cloud_resources(
            cloud_resource=new_cloud_resource,
            boto3_session=boto3_session,
            region=cloud.region,
            cloud_id=cloud_id,
            is_bring_your_own_resource=cloud.is_bring_your_own_resource,
            is_private_network=cloud.is_private_cloud
            if cloud.is_private_cloud
            else False,
        ):
            raise ClickException(
                "Cloud edit failed because resource failed verification. Please check the verification results above, fix them, and try again."
            )

        self.log.info(
            self.log.highlight(
                "Please make sure you checked the warnings from above verification results."
            )
        )
        self.log.close_block("Verify")

        self.log.open_block(
            "Reminder", "Please read the following reminder carefully..."
        )
        self.log.info(
            self.log.highlight(
                "If there are running workloads utilizing the old resources, you may want to retain them. Please note that this edit will not automatically remove any old resources. If you wish to delete them, you'll need to handle it."
            )
        )
        self.log.info(
            self.log.highlight(
                "The cloud resources we are going to edit {} ({}): \n{}".format(
                    cloud_name, cloud_id, "; \n".join(details_logs)
                )
            )
        )
        self.log.close_block("Reminder")

        confirm(
            "Are you sure you want to edit these cloud resource? ", yes,
        )

        # Execute edit cloud.
        self.log.open_block("Edit", "Start editing cloud...")
        try:
            self.api_client.edit_cloud_resource_api_v2_clouds_with_cloud_resource_router_cloud_id_patch(
                cloud_id=cloud_id,
                editable_cloud_resource=EditableCloudResource(
                    aws_s3_id=aws_s3_id,
                    aws_efs_id=aws_efs_id,
                    aws_efs_mount_target_ip=aws_efs_mount_target_ip,
                    memorydb_cluster_config=memorydb_cluster_config,
                ),
            )
        except Exception as e:  # noqa: BLE001
            self.log.error(str(e))
            raise ClickException(
                "Edit cloud resource failed! The backend server might be under maintainance right now, please reach out to support or your SA for assistance."
            )

        # Hint customer rollback command.
        rollback_command = self._generate_rollback_command(
            cloud_id, cloud_resource, edit_details
        )
        self.log.info(
            self.log.highlight(
                f"Cloud {cloud_name}({cloud_id}) is successfully edited."
            )
        )
        if rollback_command:
            self.log.info(
                self.log.highlight(
                    f"If you want to revert the edit, you can edit it back to the original cloud with: `{rollback_command}`"
                )
            )
        self.log.close_block("Edit")

    def _get_project_id(self, cloud: Any, cloud_name: str, cloud_id: str) -> str:
        try:
            return json.loads(cloud.credentials)["project_id"]
        except Exception:  # noqa: BLE001
            raise ClickException(
                f"Failed to get project id for cloud {cloud_name}({cloud_id}). Please ensure the provided cloud_name/cloud_id exists."
            )

    def _get_gcp_filestore_config(
        self,
        gcp_filestore_instance_id: str,
        gcp_filestore_location: str,
        project_id: str,
        cloud_resource: Any,
        gcp_utils,
    ) -> GCPFileStoreConfig:
        try:
            factory = gcp_utils.get_google_cloud_client_factory(self.log, project_id)
            return gcp_utils.get_gcp_filestore_config(
                factory,
                project_id,
                cloud_resource.gcp_vpc_id,
                gcp_filestore_location,
                gcp_filestore_instance_id,
                self.log,
            )
        except Exception as e:  # noqa: BLE001
            self.log.error(str(e))
            raise ClickException(
                f"Failed to construct the gcp_filestore_config from project {project_id}, please double check the provided filestore_location {gcp_filestore_location} and filestore_instance_id {gcp_filestore_instance_id}."
            )

    def _get_gcp_edit_details(
        self,
        *,
        cloud_resource: Any,
        edit_details: Dict[str, Optional[str]],
        gcp_filestore_config: GCPFileStoreConfig,
        gcp_filestore_instance_id: Optional[str],
        gcp_filestore_location: Optional[str],
        gcp_utils,
    ) -> List[str]:
        details_logs = self._generate_edit_details_logs(cloud_resource, edit_details)
        if gcp_filestore_config:
            (
                old_filestore_location,
                old_filestore_instance_id,
            ) = gcp_utils.get_filestore_location_and_instance_id(
                cloud_resource.gcp_filestore_config
            )
            if (
                old_filestore_instance_id == gcp_filestore_instance_id
                and old_filestore_location == gcp_filestore_location
            ):
                raise ClickException(
                    f"Specified resource is the same as existed resource -- gcp_filestore_instance_id: {gcp_filestore_instance_id}; gcp_filestore_location: {gcp_filestore_location}"
                )
            details_logs.append(
                f"filestore_instance_id: from {old_filestore_instance_id} -> {gcp_filestore_instance_id}"
            )
            details_logs.append(
                f"filestore_location: from {old_filestore_location} -> {gcp_filestore_location}"
            )
        return details_logs

    def _generate_rollback_command_for_gcp(
        self,
        cloud_id: str,
        cloud_resource: Any,
        edit_details: Dict[str, Optional[str]],
        gcp_filestore_config: GCPFileStoreConfig,
        gcp_utils,
    ):
        rollback_cmd = self._generate_rollback_command(
            cloud_id, cloud_resource, edit_details
        )
        if gcp_filestore_config:
            (
                old_filestore_location,
                old_filestore_instance_id,
            ) = gcp_utils.get_filestore_location_and_instance_id(
                cloud_resource.gcp_filestore_config
            )
            rollback_cmd += f" --gcp-filestore-instance-id={old_filestore_instance_id}"
            rollback_cmd += f" --gcp-filestore-location={old_filestore_location}"
        rollback_cmd = rollback_cmd.replace(
            "gcp-cloud-storage-bucket-id", "gcp-cloud-storage-bucket-name"
        )
        return rollback_cmd

    def _edit_gcp_cloud(  # noqa: PLR0912
        self,
        *,
        cloud_id: str,
        cloud_name: str,
        cloud: Any,
        cloud_resource: Any,
        gcp_filestore_instance_id: Optional[str],
        gcp_filestore_location: Optional[str],
        gcp_cloud_storage_bucket_name: Optional[str],
        memorystore_instance_name: Optional[str],
        yes: bool = False,
    ):
        project_id = self._get_project_id(cloud, cloud_name, cloud_id)
        gcp_utils = try_import_gcp_utils()

        gcp_filestore_config = None
        if gcp_filestore_instance_id and gcp_filestore_location:
            gcp_filestore_config = self._get_gcp_filestore_config(
                gcp_filestore_instance_id,
                gcp_filestore_location,
                project_id,
                cloud_resource,
                gcp_utils,
            )

        memorystore_instance_config = None
        if memorystore_instance_name:
            factory = gcp_utils.get_google_cloud_client_factory(self.log, project_id)
            memorystore_instance_config = gcp_utils.get_gcp_memorystore_config(
                factory, memorystore_instance_name
            )

        # Log edit details.
        self.log.open_block("EditDetail", "\nEdit details...")
        edit_details = {
            "gcp_cloud_storage_bucket_id": gcp_cloud_storage_bucket_name,
            "memorystore_instance_name": memorystore_instance_name,
        }
        details_logs = self._get_gcp_edit_details(
            cloud_resource=cloud_resource,
            edit_details=edit_details,
            gcp_filestore_config=gcp_filestore_config,
            gcp_filestore_instance_id=gcp_filestore_instance_id,
            gcp_filestore_location=gcp_filestore_location,
            gcp_utils=gcp_utils,
        )
        self.log.info(
            self.log.highlight(
                "Cloud edit details {} ({}): \n{}".format(
                    cloud_name, cloud_id, "; \n".join(details_logs)
                )
            )
        )
        self.log.close_block("EditDetail")

        # Static Verify.
        self.log.open_block(
            "Verify", "Start cloud static verification on the specified resources..."
        )
        new_cloud_resource = copy.deepcopy(cloud_resource)
        if gcp_filestore_config:
            new_cloud_resource.gcp_filestore_config = gcp_filestore_config
        if gcp_cloud_storage_bucket_name:
            new_cloud_resource.gcp_cloud_storage_bucket_id = (
                gcp_cloud_storage_bucket_name
            )
        if memorystore_instance_config:
            new_cloud_resource.memorystore_instance_config = memorystore_instance_config
        if not self.verify_gcp_cloud_resources(
            cloud_resource=new_cloud_resource,
            project_id=project_id,
            region=cloud.region,
            cloud_id=cloud_id,
            yes=False,
        ):
            raise ClickException(
                "Cloud edit failed because resource failed verification. Please check the verification results above, fix them, and try again."
            )

        self.log.info(
            self.log.highlight(
                "Please make sure you checked the warnings from above verification results."
            )
        )
        self.log.close_block("Verify")

        self.log.open_block(
            "Reminder", "Please read the following reminder carefully..."
        )
        self.log.info(
            self.log.highlight(
                "If there are running workloads utilizing the old resources, you may want to retain them. Please note that this edit will not automatically remove any old resources. If you wish to delete them, you'll need to handle it."
            )
        )
        self.log.info(
            self.log.highlight(
                "The cloud resources we are going to edit {} ({}): \n{}".format(
                    cloud_name, cloud_id, "; \n".join(details_logs)
                )
            )
        )
        self.log.close_block("Reminder")

        confirm(
            "Are you sure you want to edit these cloud resource? ", yes,
        )

        # Execute edit cloud.
        self.log.open_block("Edit", "Start editing cloud...")
        try:
            self.api_client.edit_cloud_resource_api_v2_clouds_with_cloud_resource_gcp_router_cloud_id_patch(
                cloud_id=cloud_id,
                editable_cloud_resource_gcp=EditableCloudResourceGCP(
                    gcp_filestore_config=gcp_filestore_config,
                    gcp_cloud_storage_bucket_id=gcp_cloud_storage_bucket_name,
                    memorystore_instance_config=memorystore_instance_config,
                ),
            )
        except Exception as e:  # noqa: BLE001
            self.log.error(str(e))
            raise ClickException(
                "Edit cloud resource failed! The backend server might be under maintainance right now, please reach out to support or your SA for assistance."
            )

        # Hint customer rollback command.
        rollback_command = self._generate_rollback_command_for_gcp(
            cloud_id, cloud_resource, edit_details, gcp_filestore_config, gcp_utils,
        )
        self.log.info(
            self.log.highlight(
                f"Cloud {cloud_name}({cloud_id}) is successfully edited."
            )
        )
        if rollback_command:
            self.log.info(
                self.log.highlight(
                    f"If you want to revert the edit, you can edit it back to the original cloud with: `{rollback_command}`"
                )
            )
        self.log.close_block("Edit")

    def edit_cloud(  # noqa: PLR0912,PLR0913
        self,
        *,
        cloud_name: Optional[str],
        cloud_id: Optional[str],
        aws_s3_id: Optional[str],
        aws_efs_id: Optional[str],
        aws_efs_mount_target_ip: Optional[str],
        memorydb_cluster_id: Optional[str],
        gcp_filestore_instance_id: Optional[str],
        gcp_filestore_location: Optional[str],
        gcp_cloud_storage_bucket_name: Optional[str],
        memorystore_instance_name: Optional[str],
        functional_verify: Optional[str],
        yes: bool = False,
    ):
        """Edit aws cloud.

        The editable fields are in EditableCloudResource (AWS) /EditableCloudResourceGCP (GCP).
        Steps:
        1. Log the edits (from old to new values).
        2. Static verify cloud resources with updated values.
        3. Prompt the customer for confirmation based on verification results.
        4. Update the cloud resource (calls backend API to modify the database).
        5. Conduct a functional verification, if specified.
        """
        functions_to_verify = self._validate_functional_verification_args(
            functional_verify
        )
        cloud_id, cloud_name = get_cloud_id_and_name(
            self.api_client, cloud_id, cloud_name
        )
        cloud = self.api_client.get_cloud_api_v2_clouds_cloud_id_get(cloud_id).result
        if not cloud.is_bring_your_own_resource:
            raise ClickException(
                f"Cloud {cloud_name}({cloud_id}) is not a cloud with customer defined resources, currently we don't support editing managed clouds."
            )

        cloud_resource = get_cloud_resource_by_cloud_id(
            cloud_id, cloud.provider, self.api_client
        )
        if cloud_resource is None:
            raise ClickException(
                f"Cloud {cloud_name}({cloud_id}) does not contain resource records."
            )
        if cloud.provider == "AWS":
            self.cloud_event_producer.init_trace_context(
                CloudAnalyticsEventCommandName.EDIT,
                CloudProviders.AWS,
                cloud_id=cloud_id,
            )
            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.COMMAND_START, succeeded=True
            )
            if (
                not any(
                    [
                        aws_s3_id,
                        aws_efs_id,
                        aws_efs_mount_target_ip,
                        memorydb_cluster_id,
                    ]
                )
            ) or any(
                [
                    gcp_filestore_instance_id,
                    gcp_filestore_location,
                    gcp_cloud_storage_bucket_name,
                    memorystore_instance_name,
                ]
            ):
                self.cloud_event_producer.produce(
                    CloudAnalyticsEventName.RESOURCES_EDITED,
                    succeeded=False,
                    internal_error="specified resource and provider mismatch",
                )
                raise ClickException(
                    "Specified resource and provider mismatch -- the cloud's provider is AWS, please make sure all the resource you want to edit is for AWS as well."
                )
            try:
                self._edit_aws_cloud(
                    cloud_id=cloud_id,
                    cloud_name=cloud_name,
                    cloud=cloud,
                    cloud_resource=cloud_resource,
                    aws_s3_id=aws_s3_id,
                    aws_efs_id=aws_efs_id,
                    aws_efs_mount_target_ip=aws_efs_mount_target_ip,
                    memorydb_cluster_id=memorydb_cluster_id,
                    yes=yes,
                )
            except Exception as e:  # noqa: BLE001
                self.cloud_event_producer.produce(
                    CloudAnalyticsEventName.RESOURCES_EDITED,
                    succeeded=False,
                    logger=self.log,
                    internal_error=str(e),
                )
                raise e
        elif cloud.provider == "GCP":
            self.cloud_event_producer.init_trace_context(
                CloudAnalyticsEventCommandName.EDIT,
                CloudProviders.GCP,
                cloud_id=cloud_id,
            )
            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.COMMAND_START, succeeded=True
            )
            if (
                not any(
                    [
                        gcp_filestore_instance_id,
                        gcp_filestore_location,
                        gcp_cloud_storage_bucket_name,
                        memorystore_instance_name,
                    ]
                )
            ) or any(
                [aws_s3_id, aws_efs_id, aws_efs_mount_target_ip, memorydb_cluster_id]
            ):
                self.cloud_event_producer.produce(
                    CloudAnalyticsEventName.RESOURCES_EDITED,
                    succeeded=False,
                    internal_error="specified resource and provider mismatch",
                )
                raise ClickException(
                    "Specified resource and provider mismatch -- the cloud's provider is GCP, please make sure all the resource you want to edit is for GCP as well."
                )
            try:
                self._edit_gcp_cloud(
                    cloud_id=cloud_id,
                    cloud_name=cloud_name,
                    cloud=cloud,
                    cloud_resource=cloud_resource,
                    gcp_filestore_instance_id=gcp_filestore_instance_id,
                    gcp_filestore_location=gcp_filestore_location,
                    gcp_cloud_storage_bucket_name=gcp_cloud_storage_bucket_name,
                    memorystore_instance_name=memorystore_instance_name,
                    yes=yes,
                )
            except Exception as e:  # noqa: BLE001
                self.cloud_event_producer.produce(
                    CloudAnalyticsEventName.RESOURCES_EDITED,
                    succeeded=False,
                    logger=self.log,
                    internal_error=str(e),
                )
                raise e
        else:
            self.cloud_event_producer.produce(
                CloudAnalyticsEventName.RESOURCES_EDITED,
                succeeded=False,
                internal_error="invalid cloud provider",
            )
            raise ClickException(
                f"Unsupported cloud provider {cloud.provider} for cloud edit!"
            )

        self.cloud_event_producer.produce(
            CloudAnalyticsEventName.RESOURCES_EDITED, succeeded=True
        )
        # Functional verify.
        if len(functions_to_verify) > 0:
            functional_verify_succeed = CloudFunctionalVerificationController(
                self.cloud_event_producer, self.log
            ).start_verification(
                cloud_id,
                self._get_cloud_provider_from_str(cloud.provider),
                functions_to_verify,
                yes,
            )
            if not functional_verify_succeed:
                raise ClickException(
                    "Cloud functional verification failed. Please consider the following options:\n"
                    "1. Create a new cloud (we recommend)\n"
                    "2. Double-check the resources specified in the edit details, and the verification results, modify the resource if necessary, run `anyscale cloud verify (optional with functional-verify)` to verify again.\n"
                    "3. Edit the resource back to original if you still want to use this cloud.\n"
                )

    ### End of edit cloud ###
