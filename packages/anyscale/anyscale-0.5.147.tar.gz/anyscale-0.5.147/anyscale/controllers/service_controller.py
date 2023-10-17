import os
from typing import List, Optional

import click
import tabulate
import yaml

from anyscale.cli_logger import BlockLogger
from anyscale.client.openapi_client import ComputeTemplate, ProductionJob
from anyscale.client.openapi_client.models.decorated_list_service_api_model import (
    DecoratedListServiceAPIModel,
)
from anyscale.client.openapi_client.models.decorated_production_service_v2_api_model import (
    DecoratedProductionServiceV2APIModel,
)
from anyscale.client.openapi_client.models.ha_job_states import HaJobStates
from anyscale.controllers.base_controller import BaseController
from anyscale.formatters.service_formatter import format_service_config_v2
from anyscale.models.service_model import ServiceConfig
from anyscale.project import infer_project_id
from anyscale.tables import ServicesTable
from anyscale.util import (
    get_endpoint,
    poll,
    populate_dict_with_workspace_config_if_exists,
)
from anyscale.utils.runtime_env import override_runtime_env_config
from anyscale.utils.workload_types import Workload


_POLL_SERVICE_VERSION_INFO_INTERVAL_IN_SECS = 3.0
_POLL_SERVICE_VERSION_INFO_TIMEOUT_IN_SECS = 60.0 * 3


class ServiceController(BaseController):
    def __init__(
        self, log: Optional[BlockLogger] = None, initialize_auth_api_client: bool = True
    ):
        if log is None:
            log = BlockLogger()

        super().__init__(initialize_auth_api_client=initialize_auth_api_client)
        self.log = log

    def _get_services_by_name(
        self,
        *,
        name: Optional[str] = None,
        project_id: Optional[str] = None,
        created_by_me: bool,
        max_items: int,
    ) -> List[DecoratedListServiceAPIModel]:
        """Makes an API call to get all services matching the provided filters.

        This returns both v1 and v2 services.
        """
        creator_id = None
        if created_by_me:
            user_info_response = self.api_client.get_user_info_api_v2_userinfo_get()
            creator_id = user_info_response.result.id

        services_list = []
        resp = self.api_client.list_services_api_v2_services_v2_get(
            project_id=project_id, name=name, creator_id=creator_id, count=10,
        )
        services_list.extend(resp.results)
        paging_token = resp.metadata.next_paging_token
        while paging_token is not None and len(services_list) < max_items:
            resp = self.api_client.list_services_api_v2_services_v2_get(
                project_id=project_id,
                name=name,
                creator_id=creator_id,
                count=10,
                paging_token=paging_token,
            )
            services_list.extend(resp.results)
            paging_token = resp.metadata.next_paging_token

        return services_list[:max_items]

    def _get_service_id_from_name(
        self, service_name: str, project_id: Optional[str]
    ) -> str:
        """Get the ID for a service by name.

        If project_id is specified, filter to that project, else don't filter on project_id and
        instead error if there are multiple services with the name.

        Raises an exception if there are zero or multiple services with the given name.
        """
        results = self._get_services_by_name(
            name=service_name, project_id=project_id, created_by_me=False, max_items=10
        )

        if len(results) == 0:
            raise click.ClickException(
                f"No service with name '{service_name}' was found. "
                "Please verify that this service exists and you have access to it."
            )
        elif len(results) > 1:
            raise click.ClickException(
                f"There are multiple services with name '{service_name}'. "
                "Please filter using --project-id or specify the --service-id instead. "
                f"Services found: \n{ServicesTable(results)}"
            )

        return results[0].id

    def get_service_id(
        self,
        *,
        service_id: Optional[str] = None,
        service_name: Optional[str] = None,
        service_config_file: Optional[str] = None,
        project_id: Optional[str] = None,
    ) -> str:
        """Get the service ID given the ID, name, or config file.

        This is a utility used by multiple CLI commands to standardize mapping these options
        to a service_id.

        The precedence is: service_id > service_name > service_config_file.

        If the project_id is specified directly or via the service_config_file it will be used
        to filter the query. Else we will try to find the service across all projects and error
        if there are multiple.
        """
        if service_id is not None:
            if service_name is not None or service_config_file is not None:
                raise click.ClickException(
                    "Only one of service ID, name, or config file should be specified."
                )
        elif service_name is not None:
            if service_config_file is not None:
                raise click.ClickException(
                    "Only one of service ID, name, or config file should be specified."
                )
            service_id = self._get_service_id_from_name(service_name, project_id)
        elif service_config_file is not None:
            service_config: ServiceConfig = self._read_service_config_file(
                service_config_file
            )
            # Allow the passed project_id to override the one in the file.
            project_id = project_id or service_config.project_id
            service_id = self._get_service_id_from_name(service_config.name, project_id)
        else:
            raise click.ClickException(
                "Service ID, name, or config file must be specified."
            )

        return service_id

    def generate_config_from_file(
        self,
        service_config_file,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
        version: Optional[str] = None,
        canary_percent: Optional[int] = None,
        rollout_strategy: Optional[str] = None,
    ) -> ServiceConfig:
        """
        Given the input file path and user overrides, this method
        constructs the expected service configuration.

        Note that if the command is run from a workspace, some values
        may be overwritten.
        """
        service_config: ServiceConfig = self._read_service_config_file(
            service_config_file
        )
        if name:
            service_config.name = name

        if description:
            service_config.description = description

        if version:
            service_config.version = version

        if canary_percent is not None:
            service_config.canary_percent = canary_percent

        if rollout_strategy:
            service_config.rollout_strategy = rollout_strategy

        if service_config.rollout_strategy:
            service_config.rollout_strategy = service_config.rollout_strategy.upper()

        return service_config

    def _get_maximum_uptime_minutes(self, service: ProductionJob) -> Optional[int]:
        compute_config: ComputeTemplate = self.api_client.get_compute_template_api_v2_compute_templates_template_id_get(
            service.config.compute_config_id
        ).result
        return compute_config.config.maximum_uptime_minutes

    def _get_maximum_uptime_output(self, maximum_uptime_minutes: Optional[int]) -> str:
        if maximum_uptime_minutes and maximum_uptime_minutes > 0:
            return f"set to {maximum_uptime_minutes} minutes"
        return "disabled"

    def _get_additional_log_if_maximum_uptime_enabled(
        self, maximum_uptime_minutes: Optional[int]
    ) -> str:
        if maximum_uptime_minutes and maximum_uptime_minutes > 0:
            return " This may cause disruptions. To disable, update the compute config."
        return ""

    def _read_service_config_file(self, service_config_file: str) -> ServiceConfig:
        if not os.path.exists(service_config_file):
            raise click.ClickException(f"Config file {service_config_file} not found.")

        with open(service_config_file) as f:
            config_dict = yaml.safe_load(f)

        updated_config_dict = populate_dict_with_workspace_config_if_exists(
            config_dict, self.anyscale_api_client
        )
        return ServiceConfig.parse_obj(updated_config_dict)

    def rollout(
        self,
        service_config_file: str,
        name: Optional[str] = None,
        version: Optional[str] = None,
        canary_percent: Optional[int] = None,
        rollout_strategy: Optional[str] = None,
    ):
        """
        Deploys a Service 2.0.
        """
        config = self.generate_config_from_file(
            service_config_file,
            name=name,
            version=version,
            canary_percent=canary_percent,
            rollout_strategy=rollout_strategy,
        )

        config.project_id = infer_project_id(
            self.anyscale_api_client,
            self.api_client,
            self.log,
            project_id=config.project_id,
            cluster_compute_id=config.compute_config_id,
            cluster_compute=config.compute_config,
            cloud=config.cloud,
            cluster_compute_version=config.compute_config_version,
        )

        service_config = config.config
        if service_config:
            access_config = service_config.get("access", {})

            if (
                isinstance(access_config, dict)
                and access_config.get("use_bearer_token", True) is False
            ):
                self.log.warning(
                    "Using bearer token for authorization is disabled: no authorization guarding will be used for this service."
                )

        if not config.ray_serve_config:
            config.ray_serve_config = {}

        self._overwrite_runtime_env_in_v2_ray_serve_config(config)

        service_v2_config = format_service_config_v2(config)

        service = self.api_client.apply_service_v2_api_v2_services_v2_apply_put(
            service_v2_config
        ).result

        current_state = service.goal_state
        self.log.info(
            f"Service {service.id} has been deployed. Service is transitioning towards: {current_state}."
        )
        self.log.info(
            f'View the service in the UI at {get_endpoint(f"/services/{service.id}")}'
        )

        if config.canary_percent is not None and len(service.versions) > 1:
            if config.canary_percent == 100:
                self.log.warning(
                    "The canary percent has been set to 100%. This will complete the rollout."
                )
            self._log_canary_version_query(service)

    def _overwrite_runtime_env_in_v2_ray_serve_config(self, config: ServiceConfig):
        """Modifies config in place."""
        ray_serve_config = config.ray_serve_config
        if "applications" in ray_serve_config:
            for ray_serve_app_config in ray_serve_config["applications"]:
                ray_serve_app_config["runtime_env"] = override_runtime_env_config(
                    runtime_env=ray_serve_app_config.get("runtime_env"),
                    anyscale_api_client=self.anyscale_api_client,
                    api_client=self.api_client,
                    workload_type=Workload.SERVICES,
                    compute_config_id=config.compute_config_id,
                    log=self.log,
                )

        else:
            ray_serve_config["runtime_env"] = override_runtime_env_config(
                runtime_env=ray_serve_config.get("runtime_env"),
                anyscale_api_client=self.anyscale_api_client,
                api_client=self.api_client,
                workload_type=Workload.SERVICES,
                compute_config_id=config.compute_config_id,
                log=self.log,
            )

    def _log_canary_version_query(self, service: DecoratedProductionServiceV2APIModel):
        """
        This method logs the canary version's query endpoint.

        Since the url and token from the service object are not initially available,
        we poll until they become available.
        """
        assert len(service.versions) > 1
        # We assume versions are returned in order of creation.
        canary_version = service.versions[1]
        production_job_id = (
            canary_version.production_job_ids[0]
            if canary_version.production_job_ids
            else None
        )
        if production_job_id:
            canary_version_query_printed = False
            for _ in poll(
                interval_secs=_POLL_SERVICE_VERSION_INFO_INTERVAL_IN_SECS,
                timeout_secs=_POLL_SERVICE_VERSION_INFO_TIMEOUT_IN_SECS,
            ):
                try:
                    service_v1 = self.api_client.get_job_api_v2_decorated_ha_jobs_production_job_id_get(
                        production_job_id
                    ).result
                    url = service_v1.url
                    token = service_v1.token
                    service_version_current_state = service_v1.state.current_state
                    if url and token:
                        self.log.info()
                        self.log.info(
                            "You can query the service endpoint using the curl request below:"
                        )
                        self.log.info(f"curl -H 'Authorization: Bearer {token}' {url}")

                        if service_version_current_state in {
                            HaJobStates.PENDING,
                            HaJobStates.AWAITING_CLUSTER_START,
                        }:
                            self.log.info(
                                "Please note the canary version is still pending and may take several minutes to begin successfully returning requests."
                            )
                        canary_version_query_printed = True
                        break
                except Exception:  # noqa: BLE001
                    # We keep re-retrying until the timeout
                    pass
            if not canary_version_query_printed:
                self.log.info(
                    "Please refer to the Service details page if you would like to query the canary version."
                )

    def list(
        self,
        *,
        name: Optional[str] = None,
        service_id: Optional[str] = None,
        project_id: Optional[str] = None,
        created_by_me: bool = False,
        max_items: int = 10,
    ) -> None:
        self._list_via_service_list_endpoint(
            name=name,
            service_id=service_id,
            project_id=project_id,
            created_by_me=created_by_me,
            max_items=max_items,
        )

    def _list_via_service_list_endpoint(
        self,
        *,
        name: Optional[str] = None,
        service_id: Optional[str] = None,
        project_id: Optional[str] = None,
        created_by_me: bool = False,
        max_items: int,
    ):
        services = []
        if service_id:
            service_v2_result: DecoratedProductionServiceV2APIModel = (
                self.api_client.get_service_api_v2_services_v2_service_id_get(
                    service_id
                ).result
            )
            services.append(
                [
                    service_v2_result.name,
                    service_v2_result.id,
                    service_v2_result.current_state,
                    # TODO: change to email once https://github.com/anyscale/product/pull/18189 is merged
                    service_v2_result.creator_id,
                ]
            )

        else:
            services_data = self._get_services_by_name(
                name=name,
                project_id=project_id,
                created_by_me=created_by_me,
                max_items=max_items,
            )

            services = [
                [
                    service.name,
                    service.id,
                    service.current_state,
                    service.creator.email,
                ]
                for service in services_data
            ]

        table = tabulate.tabulate(
            services,
            headers=["NAME", "ID", "CURRENT STATE", "CREATOR"],
            tablefmt="plain",
        )
        self.log.info(f'View your Services in the UI at {get_endpoint("/services")}')
        self.log.info(f"Services:\n{table}")

    def archive(self, service_id: str):
        raise click.ClickException(
            f"Archive {service_id} is not currently supported for v2 services."
            "Please contact Anyscale support for more information."
        )

    def rollback(self, service_id: str) -> None:
        service = self.api_client.rollback_service_api_v2_services_v2_service_id_rollback_post(
            service_id
        ).result

        self.log.info(f"Service {service.id} rollback initiated.")
        self.log.info(
            f'View the service in the UI at {get_endpoint(f"/services/{service.id}")}'
        )

    def terminate(self, service_id: str) -> None:
        self.api_client.terminate_service_api_v2_services_v2_service_id_terminate_post(
            service_id
        )
        self.log.info(f"Service {service_id} terminate initiated.")
        self.log.info(
            f'View the service in the UI at {get_endpoint(f"/services/{service_id}")}'
        )
