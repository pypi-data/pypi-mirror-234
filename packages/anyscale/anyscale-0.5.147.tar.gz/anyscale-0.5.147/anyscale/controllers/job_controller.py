from abc import ABC, abstractmethod
import asyncio
import contextlib
from datetime import datetime, timedelta
import json
import os
import random
import string
import time
import traceback
from typing import Any, Callable, cast, Dict, List, Optional, Tuple, Union

import click
from pydantic import BaseModel
import requests
from requests.adapters import HTTPAdapter
import tabulate
from urllib3 import Retry
import yaml

from anyscale.api_utils.exceptions.log_retrieval_errors import (
    ExpectedLogRetrievalError,
    wrap_as_unsupported_log_retrieval_method_error,
    wrap_job_run_log_not_retrievable_on_active_cluster_error,
)
from anyscale.api_utils.job_logs_util import (
    _get_job_logs_from_storage_bucket,
    _get_job_logs_from_storage_bucket_streaming,
    _get_logs_from_active_job_run,
)
from anyscale.api_utils.logs_util import _stream_log_from_ray_websocket
from anyscale.cli_logger import LogsLogger
from anyscale.client.openapi_client import (
    ComputeTemplate,
    ProductionJob,
    ProductionJobConfig,
)
from anyscale.client.openapi_client.models.create_internal_production_job import (
    CreateInternalProductionJob,
)
from anyscale.client.openapi_client.models.decorated_production_job import (
    DecoratedProductionJob,
)
from anyscale.client.openapi_client.models.ha_job_states import HaJobStates
from anyscale.controllers.base_controller import BaseController
from anyscale.models.job_model import JobConfig
from anyscale.project import infer_project_id
from anyscale.sdk.anyscale_client.models.job import Job
from anyscale.sdk.anyscale_client.models.jobs_query import JobsQuery
from anyscale.sdk.anyscale_client.models.jobs_sort_field import JobsSortField
from anyscale.sdk.anyscale_client.models.page_query import PageQuery
from anyscale.sdk.anyscale_client.models.sort_by_clause_jobs_sort_field import (
    SortByClauseJobsSortField,
)
from anyscale.sdk.anyscale_client.models.sort_order import SortOrder
from anyscale.util import (
    get_endpoint,
    handle_and_log_lines_in_click_exception,
    is_anyscale_workspace,
    poll,
    populate_dict_with_workspace_config_if_exists,
    validate_job_config_dict,
)
from anyscale.utils.connect_helpers import search_entities
from anyscale.utils.runtime_env import override_runtime_env_config
from anyscale.utils.workload_types import Workload


log = LogsLogger()

_TERMINAL_STATES = {
    HaJobStates.SUCCESS,
    HaJobStates.TERMINATED,
    HaJobStates.BROKEN,
    HaJobStates.OUT_OF_RETRIES,
}
_PENDING_STATES = {
    HaJobStates.PENDING,
    HaJobStates.AWAITING_CLUSTER_START,
    HaJobStates.ERRORED,
    HaJobStates.RESTARTING,
}


class MiniJobRun(BaseModel):
    last_job_run_id: str
    job_state: str
    error: Optional[str]


class LogProvider(ABC):
    @abstractmethod
    def __init__(self, dns_name: str, anyscale_token: str, query: str) -> None:
        pass

    @abstractmethod
    def query(
        self, start_timestamp_ns: int, end_timestamp_ns: int
    ) -> List[Tuple[int, str]]:
        """Query logs for a time range, return list of (timestamp_ns, log_line)."""

    @abstractmethod
    def close(self) -> None:
        """Close any connection this log provider uses"""

    def __enter__(self, *args, **kwargs):  # noqa: B027
        pass

    def __exit__(self, *args, **kwargs):
        self.close()


class LokiLogProvider(LogProvider):
    def __init__(self, dns_name: str, anyscale_token: str, query: str) -> None:
        # https://grafana.com/docs/loki/latest/api/#get-lokiapiv1query_range
        self.url = f"https://{dns_name}/loki/api/v1/query_range"
        self.params: Dict[str, Union[str, int]] = {
            "token": anyscale_token,
            "query": query,
            "limit": 1000,
            "start": 0,
            "end": int(time.time() * 1e9),
            "direction": "forward",
        }

    def __enter__(self, *args, **kwargs):
        self.session = requests.Session()
        self.session.mount(
            "https://",
            HTTPAdapter(
                max_retries=Retry(total=10, backoff_factor=0.1, allowed_methods=["GET"])
            ),
        )
        return self

    def close(self) -> None:
        self.session.close()

    def __exit__(self, *args, **kwargs):
        self.close()

    def query(
        self, start_timestamp_ns: int, end_timestamp_ns: int
    ) -> List[Tuple[int, str]]:
        if start_timestamp_ns == 0:
            # 10^9 nanoseconds in a second
            start_timestamp_ns = int(
                (datetime.now() - timedelta(days=7)).timestamp() * (10 ** 9)
            )
        self.params["start"] = start_timestamp_ns
        self.params["end"] = end_timestamp_ns

        resp = self.session.get(self.url, params=self.params)
        resp.raise_for_status()

        resp_data = resp.json()
        if resp_data["status"] != "success":
            raise click.ClickException("Querying Anyscale log endpoint failed.")
        if resp_data["data"]["resultType"] != "streams":
            raise click.ClickException("Invalid metrics type.")

        lines = []
        for log_chunk in resp_data["data"]["result"]:
            # TODO(simon): potentially annotate the log with the log_chunk["stream"] metadata
            for timestamp, line in log_chunk["values"]:
                lines.append((int(timestamp), line))

        return lines


class JobController(BaseController):
    def __init__(
        self,
        log: Optional[LogsLogger] = None,
        initialize_auth_api_client: bool = True,
        raise_structured_exception: bool = False,
    ):
        if log is None:
            log = LogsLogger()

        super().__init__(initialize_auth_api_client, raise_structured_exception)
        self.log = log
        self.log.open_block("Output")
        self._cluster_journal_events_start_line = 0

    def submit(
        self,
        job_config_file: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        is_entrypoint_cmd: Optional[bool] = False,
        entrypoint: Optional[List[str]] = None,
    ) -> str:
        entrypoint = entrypoint or []
        workspace_id = os.environ.get("ANYSCALE_EXPERIMENTAL_WORKSPACE_ID", None)
        if is_anyscale_workspace() and is_entrypoint_cmd:
            entrypoint = [job_config_file, *entrypoint]
            config = self.generate_config_from_entrypoint(
                entrypoint, name, description, workspace_id
            )
            id = self.submit_from_config(config)  # noqa: A001
        elif len(entrypoint) == 0:
            # Assume that job_config_file is a file and submit it.
            config = self.generate_config_from_file(
                job_config_file,
                name=name,
                description=description,
                workspace_id=workspace_id,
            )
            id = self.submit_from_config(config)  # noqa: A001
        elif len(entrypoint) != 0:
            msg = (
                "Within an Anyscale Workspace, `anyscale job submit` takes either a file, or a command. To submit a command, use `anyscale job submit -- my command`."
                if is_anyscale_workspace()
                else "`anyscale job submit` takes one argument, a YAML file configuration. Please use `anyscale job submit my_file`."
            )
            raise click.ClickException(msg)
        return id

    def generate_config_from_entrypoint(
        self,
        entrypoint: List[str],
        name: Optional[str],
        description: Optional[str],
        workspace_id: Optional[str] = None,
    ) -> JobConfig:
        config_dict = {
            "entrypoint": " ".join(entrypoint),
            "name": name,
            "description": description,
            "workspace_id": workspace_id,
        }
        config_dict = populate_dict_with_workspace_config_if_exists(
            config_dict, self.anyscale_api_client
        )
        job_config = JobConfig.parse_obj(config_dict)
        return job_config

    def generate_config_from_file(
        self,
        job_config_file: str,
        name: Optional[str],
        description: Optional[str],
        workspace_id: Optional[str] = None,
    ) -> JobConfig:
        config_dict = self._load_config_dict_from_file(job_config_file)
        config_dict["workspace_id"] = workspace_id
        validate_job_config_dict(config_dict, self.api_client)
        config_dict = populate_dict_with_workspace_config_if_exists(
            config_dict, self.anyscale_api_client
        )
        job_config = JobConfig.parse_obj(config_dict)

        if name:
            job_config.name = name

        if description:
            job_config.description = description

        return job_config

    def submit_from_config(self, job_config: JobConfig):
        # If project id is not specified, try to infer it
        project_id = infer_project_id(
            self.anyscale_api_client,
            self.api_client,
            self.log,
            project_id=job_config.project_id,
            cluster_compute_id=job_config.compute_config_id,
            cluster_compute=job_config.compute_config,
            cloud=job_config.cloud,
            cluster_compute_version=job_config.compute_config_version,
        )

        job_config.runtime_env = override_runtime_env_config(
            runtime_env=job_config.runtime_env,
            anyscale_api_client=self.anyscale_api_client,
            api_client=self.api_client,
            workload_type=Workload.JOBS,
            compute_config_id=job_config.compute_config_id,
            log=self.log,
        )
        config_object = ProductionJobConfig(
            entrypoint=job_config.entrypoint,
            runtime_env=job_config.runtime_env,
            build_id=job_config.build_id,
            compute_config_id=job_config.compute_config_id,
            max_retries=job_config.max_retries,
        )

        job = self.api_client.create_job_api_v2_decorated_ha_jobs_create_post(
            CreateInternalProductionJob(
                name=job_config.name or self._generate_random_job_name(),
                description=job_config.description or "Job submitted from CLI",
                project_id=project_id,
                workspace_id=job_config.workspace_id,
                config=config_object,
            )
        ).result
        self.log.info(
            f"Maximum uptime is {self._get_maximum_uptime_output(job)} for clusters launched by this job."
        )
        self.log.info(
            f"Job {job.id} has been successfully submitted. Current state of job: {job.state.current_state}."
        )
        self.log.info(
            f"Query the status of the job with `anyscale job list --job-id {job.id}`."
        )
        self.log.info(
            f"Get the logs for the job with `anyscale job logs --job-id {job.id} --follow`."
        )
        self.log.info(f'View the job in the UI at {get_endpoint(f"/jobs/{job.id}")}')
        return job.id

    def _get_maximum_uptime_output(self, job: ProductionJob) -> str:
        compute_config: ComputeTemplate = self.api_client.get_compute_template_api_v2_compute_templates_template_id_get(
            job.config.compute_config_id
        ).result
        maximum_uptime_minutes = compute_config.config.maximum_uptime_minutes
        if maximum_uptime_minutes and maximum_uptime_minutes > 0:
            return f"set to {maximum_uptime_minutes} minutes"
        return "disabled"

    def _load_config_dict_from_file(self, job_config_file: str) -> Dict[str, Any]:
        if not os.path.exists(job_config_file):
            raise click.ClickException(f"Config file {job_config_file} not found.")

        with open(job_config_file) as f:
            config_dict = yaml.safe_load(f)
        return config_dict

    def wait(
        self,
        job_name: Optional[str] = None,
        job_id: Optional[str] = None,
        target_state: str = HaJobStates.SUCCESS,
        interval_secs: float = 10.0,
        timeout_secs=None,
    ):
        if target_state not in HaJobStates.allowable_values:
            raise click.ClickException(
                f"`{target_state}` is not a valid Job state. Allowed states are {HaJobStates.allowable_values}"
            )
        job_id_or_name = job_name or job_id
        job_id = cast(str, self._resolve_job_object(job_id, job_name).id,)
        with self.log.spinner(f"Waiting for Job `{job_id_or_name}`...") as spinner:
            state = None
            for _ in poll(interval_secs=interval_secs, timeout_secs=timeout_secs):
                state = self._get_job_state(job_id)
                spinner.text = f"Job `{job_id_or_name}` is in state `{state}`. Waiting to reach state `{target_state}`."

                if state == target_state:
                    spinner.succeed(
                        f"Job `{job_id_or_name}` reached state `{target_state}`."
                    )
                    return job_id

                if state in _TERMINAL_STATES:
                    msg = f"Job `{job_id_or_name}` reached terminal state `{state}`, and will not reach `{target_state}`."
                    spinner.fail(msg)
                    raise click.ClickException(msg)

            msg = f"Timed out after waiting for {timeout_secs} seconds. The current state is {state}."
            spinner.fail(msg)
            raise click.ClickException(msg)

    def _get_job_state(self, job_id: str):
        job = self.api_client.get_job_api_v2_decorated_ha_jobs_production_job_id_get(
            job_id
        ).result
        return job.state.current_state

    def list(  # noqa: PLR0913
        self,
        include_all_users: bool,
        name: Optional[str],
        job_id: Optional[str],
        project_id: Optional[str],
        include_archived: bool,
        max_items: int,
    ) -> None:
        """
        This function will list jobs.
        """
        print(f'View your Jobs in the UI at {get_endpoint("/jobs")}')

        jobs_list = []
        if job_id:
            job = self.api_client.get_job_api_v2_decorated_ha_jobs_production_job_id_get(
                job_id
            ).result
            if job.is_service:
                # `job_id` belongs to a service, but this function should list jobs.
                raise click.ClickException(
                    f"ID {job_id} belongs to a Anyscale service. Please get information about "
                    f"this service with `anyscale service list --service-id {job_id}`."
                )

            output_map = {
                "Name": job.name,
                "Id": job.id,
                "Cost (dollars)": job.cost_dollars,
                "Project name": job.project.name,
                "Cluster name": job.last_job_run.cluster.name
                if job.last_job_run and job.last_job_run.cluster
                else None,
                "Current state": job.state.current_state,
                "Creator": job.creator.email,
                "Entrypoint": job.config.entrypoint
                if len(job.config.entrypoint) < 100
                else job.config.entrypoint[:100] + " ...",
            }
            output_str = "\n".join(
                [f"\t{key}: {output_map[key]}" for key in output_map]
            )
            print(output_str)
            return
        else:
            if not include_all_users:
                creator_id = (
                    self.api_client.get_user_info_api_v2_userinfo_get().result.id
                )
            else:
                creator_id = None
            resp = self.api_client.list_decorated_jobs_api_v2_decorated_ha_jobs_get(
                project_id=project_id,
                name=name,
                creator_id=creator_id,
                type_filter="BATCH_JOB",
                archive_status="ALL" if include_archived else "NOT_ARCHIVED",
                count=10,
            )
            jobs_list.extend(resp.results)
            paging_token = resp.metadata.next_paging_token
            has_more = (paging_token is not None) and (len(jobs_list) < max_items)
            while has_more:
                resp = self.api_client.list_decorated_jobs_api_v2_decorated_ha_jobs_get(
                    project_id=project_id,
                    name=name,
                    creator_id=creator_id,
                    type_filter="BATCH_JOB",
                    archive_status="ALL" if include_archived else "NOT_ARCHIVED",
                    count=10,
                    paging_token=paging_token,
                )
                jobs_list.extend(resp.results)
                paging_token = resp.metadata.next_paging_token
                has_more = (paging_token is not None) and (len(jobs_list) < max_items)
            jobs_list = jobs_list[:max_items]

        jobs_table = [
            [
                job.name,
                job.id,
                job.cost_dollars,
                job.project.name,
                job.last_job_run.cluster.name
                if job.last_job_run and job.last_job_run.cluster
                else None,
                job.state.current_state,
                job.creator.email,
                job.config.entrypoint
                if len(job.config.entrypoint) < 50
                else job.config.entrypoint[:50] + " ...",
            ]
            for job in jobs_list
        ]

        table = tabulate.tabulate(
            jobs_table,
            headers=[
                "NAME",
                "ID",
                "COST",
                "PROJECT NAME",
                "CLUSTER NAME",
                "CURRENT STATE",
                "CREATOR",
                "ENTRYPOINT",
            ],
            tablefmt="plain",
        )
        print(f"JOBS:\n{table}")

    def archive(self, job_id: Optional[str], job_name: Optional[str]) -> None:
        """
        This function will archive jobs.
        """
        job_resp: DecoratedProductionJob = self._resolve_job_object(job_id, job_name)
        self.api_client.archive_job_api_v2_decorated_ha_jobs_production_job_id_archive_post(
            job_resp.id
        )
        self.log.info(f"Job {job_resp.id} is successfully archived.")

    def terminate(self, job_id: Optional[str], job_name: Optional[str]) -> None:
        """
        This function will terminate jobs.
        """
        job_resp: DecoratedProductionJob = self._resolve_job_object(job_id, job_name)
        job = self.api_client.terminate_job_api_v2_decorated_ha_jobs_production_job_id_terminate_post(
            job_resp.id
        ).result
        self.log.info(f"Job {job.id} has begun terminating...")
        self.log.info(
            f" Current state of Job: {job.state.current_state}. Goal state of Job: {job.state.goal_state}"
        )
        self.log.info(
            f"Query the status of the Job with `anyscale job list --job-id {job.id}`."
        )

    def _resolve_job_object(
        self, job_id: Optional[str], job_name: Optional[str]
    ) -> DecoratedProductionJob:
        """Given job_id or job_name, retrieve decorated ha job spec"""
        if job_id is None and job_name is None:
            raise click.ClickException(
                "Either `--id` or `--name` must be passed in for Job."
            )
        if job_id:
            return self._get_job(job_id)

        jobs_list_resp: List[
            DecoratedProductionJob
        ] = self.api_client.list_decorated_jobs_api_v2_decorated_ha_jobs_get(
            name=job_name, type_filter="BATCH_JOB",
        ).results
        if len(jobs_list_resp) == 0:
            raise click.ClickException(
                f"No Job found with name {job_name}. Please either pass `--id` or list the "
                f"available Jobs with `anyscale job list`."
            )
        if len(jobs_list_resp) > 1:
            raise click.ClickException(
                f"Multiple Jobs found with name {job_name}. Please specify the `--id` instead."
            )
        return jobs_list_resp[0]

    def _get_job(self, job_id: str) -> DecoratedProductionJob:
        job_object = self.api_client.get_job_api_v2_decorated_ha_jobs_production_job_id_get(
            production_job_id=job_id
        ).result
        return job_object

    def _get_formatted_latest_job_run(
        self, job: DecoratedProductionJob
    ) -> Optional[MiniJobRun]:
        job_state = job.state.current_state
        last_job_run_id = job.last_job_run_id
        if job_state in _TERMINAL_STATES and last_job_run_id is None:
            raise click.ClickException(
                f"Can't find latest job run for {job_state} job."
            )
        if not last_job_run_id:
            return None
        return MiniJobRun(
            last_job_run_id=last_job_run_id, job_state=job_state, error=job.state.error
        )

    def _wait_for_a_job_run(
        self, job_id: Optional[str], job_name: Optional[str]
    ) -> DecoratedProductionJob:
        """Waits until the job has a job run and is in a non-pending state
        (encountered when initially submitting).

        Returns the job."""
        start = time.monotonic()
        job = self._resolve_job_object(job_id, job_name)
        last_job_run_id: str = job.last_job_run_id
        job_state = job.state.current_state
        with self.log.spinner("Waiting for job run...") as spinner:
            while last_job_run_id is None or job_state in _PENDING_STATES:
                if job_state in _TERMINAL_STATES:
                    raise click.ClickException(
                        f"Can't find latest job run for {job_state} job."
                    )
                if self._cluster_journal_events_start_line == 0:
                    spinner.text = (
                        f"Waiting for a job run, current state is {job_state}..."
                    )
                time.sleep(max(0, 3 - (time.monotonic() - start)))
                start = time.monotonic()
                job = self._get_job(job.id)
                last_job_run_id = job.last_job_run_id
                if job.state.cluster_id:
                    # Once we have a cluster id, we start printing the cluster journal event logs with each loop.
                    cluster_journal_events = self._api_client.get_startup_logs_api_v2_sessions_session_id_startup_logs_get(
                        job.state.cluster_id,
                        start_line=self._cluster_journal_events_start_line,
                        end_line=10000000,
                    ).result
                    lines = cluster_journal_events.lines.splitlines()
                    if len(lines):
                        spinner.succeed("Job run found. Cluster launching...")
                    self._cluster_journal_events_start_line = (
                        cluster_journal_events.start_line
                        + cluster_journal_events.num_lines
                    )

                    for line in lines:
                        self.log.info(line)

                job_state = job.state.current_state
        return job

    def _print_logs_for_active_job_run(
        self, job_run_id: str, should_follow: bool
    ) -> None:
        """
        Prints logs from the active cluster the job is run on.
        """
        with handle_and_log_lines_in_click_exception(log_callback=self.log.error):
            if should_follow:
                # Use websockets (to continuously poll logs)
                with wrap_as_unsupported_log_retrieval_method_error():
                    websocket_url: str = self.api_client.get_job_logs_stream_api_v2_logs_job_logs_stream_job_id_get(
                        job_id=job_run_id
                    ).result.stream_url

                with wrap_job_run_log_not_retrievable_on_active_cluster_error(
                    job_run_id, raise_connection_issue_as_cli_error=True
                ):
                    # (run_until_complete() is used here b/c the KeyboardInterrupt exception is
                    # not propogated all the way up (and likely being handled by internals of asyncio.run()))
                    asyncio.get_event_loop().run_until_complete(
                        _stream_log_from_ray_websocket(
                            websocket_url,
                            log_callback=self.log.log,
                            remove_escape_chars=False,
                        )
                    )
            else:
                # Make a one-time request to get logs
                logs = asyncio.run(
                    _get_logs_from_active_job_run(
                        self.anyscale_api_client,
                        job_run_id,
                        raise_connection_issue_as_cli_error=True,
                        remove_escape_chars=False,
                    )
                )
                for line in logs.splitlines():
                    self.log.log(line)

    def _print_logs_for_inactive_job_run(self, job_run_id: str) -> None:
        """Retrieves logs from the cloud storage bucket for a job run in terminal state"""
        logs = ""
        with self.log.spinner("Retrieving logs..."):
            # For jobs on a cluster that is terminating, the logs are in-flight between cluster and storage bucket
            # of the cloud. In that case, wait for a bit and try again.
            for _ in poll(interval_secs=5, max_iter=10):
                logs = asyncio.run(
                    _get_job_logs_from_storage_bucket(
                        self.anyscale_api_client,
                        job_run_id=job_run_id,
                        remove_escape_chars=False,
                    )
                )
                if logs:
                    break
        if not logs:
            self.log.error("Logs are not available for this job run.")
            return
        for line in logs.splitlines():
            self.log.log(line)

    def _print_logs_using_streaming_job_logs(
        self, job_run_id: str, follow: bool = False
    ) -> None:
        """Retrieves logs from the streaming job logs folder in S3/GCS"""
        logs = ""
        next_page_token = None
        # Keep track of if any logs have been printed yet,
        # If not, we assume the cluster recently launched and we
        # give more leeway for the logs to be available.
        have_jobs_started_producing_logs = False
        with self.log.spinner("Retrieving logs..."):
            (
                logs,
                next_page_token,
                cluster_journal_events_start_line,
                job_finished,
            ) = asyncio.run(
                _get_job_logs_from_storage_bucket_streaming(
                    self._api_client,
                    self.log,
                    job_run_id=job_run_id,
                    remove_escape_chars=False,
                    next_page_token=next_page_token,
                    cluster_journal_events_start_line=self._cluster_journal_events_start_line,
                )
            )

        if len(logs):
            have_jobs_started_producing_logs = True

        for line in logs.splitlines():
            self.log.log(line)

        # Continuously poll for logs.
        terminal_state_count = 0
        while follow:
            start = time.monotonic()
            if job_finished:
                # Let's wait before terminating the loop to give the logs a chance to catch up.
                terminal_state_count += 1
                # Once jobs produce logs, we know we do not have to wait as long for those logs
                # to be uploaded to S3 since the cluster is already running.
                max_iterations = 4 if have_jobs_started_producing_logs else 6
                if terminal_state_count >= max_iterations:
                    self.log.info("Job run reached terminal state.")
                    return

            (
                logs,
                next_page_token,
                cluster_journal_events_start_line,
                job_finished,
            ) = asyncio.run(
                _get_job_logs_from_storage_bucket_streaming(
                    self._api_client,
                    self.log,
                    job_run_id=job_run_id,
                    remove_escape_chars=False,
                    next_page_token=next_page_token,
                    cluster_journal_events_start_line=cluster_journal_events_start_line,
                )
            )

            for line in logs.splitlines():
                self.log.log(line)

            # Wait at least 5 seconds between iterations.
            time.sleep(max(0, 5 - (time.monotonic() - start)))

    def logs(
        self,
        job_id: Optional[str] = None,
        job_name: Optional[str] = None,
        should_follow: bool = False,
        all_attempts: bool = False,
    ) -> None:
        """Uses fallback logic to print logs for a (production) job to terminal output.

        * If the job is running, it will retrieve logs from the cluster the job is run on.
        * If the job is not running, it will retrieve logs from Anyscale's backend cache.
        * If the logs no longer live in the cache, or the cloud the job is on is using Anyscale V2,
            it falls back to retrieving logs from the storage bucket of the cloud.
        """
        # This logic will be simplified once the migration to Anyscale V2 is complete.
        job = self._wait_for_a_job_run(job_id, job_name)
        is_streaming_job_logs_on = self._api_client.check_is_feature_flag_on_api_v2_userinfo_check_is_feature_flag_on_get(
            "ray-job-log-streaming"
        ).result.is_on
        last_job_run_id: str = job.last_job_run_id
        job_state: HaJobStates = job.state.current_state
        job_run_ids: List[str] = (
            [last_job_run_id]
            if not all_attempts
            else [job_run.id for job_run in self._get_all_job_runs(job.id)]
        )  # type: ignore
        for job_run_id in job_run_ids:
            self.log.open_block(
                job_run_id, f"Job Run Id: {job_run_id}", auto_close=True,
            )
            if is_streaming_job_logs_on:
                # New path for retrieving logs. Works regardless if cluster is running or dead.
                self._print_logs_using_streaming_job_logs(
                    job_run_id, follow=should_follow and job_run_id == last_job_run_id
                )
            else:
                # 1. Last job run, and 2. job is RUNNING implies (==) job run is RUNNING
                is_last_job_run_and_active = (
                    job_run_id == last_job_run_id and job_state == HaJobStates.RUNNING
                )

                get_logs_fns: List[Callable[[], None]] = [
                    *(
                        # If the job run is RUNNING, retrieve logs from the active cluster
                        []
                        if not is_last_job_run_and_active
                        else [
                            lambda: self._print_logs_for_active_job_run(
                                job_run_id, should_follow  # noqa: B023
                            )
                        ]
                    ),
                    # If the previous retrieval method failed or the job is not running
                    # retrieve logs from Anyscale's cache
                    lambda: self._print_logs_for_inactive_job_run(
                        job_run_id  # noqa: B023
                    ),
                ]
                for fn in get_logs_fns:
                    with contextlib.suppress(ExpectedLogRetrievalError):
                        fn()
                        # If `fn` didn't raise `ExpectedLogRetrievalError`, we assume logs were successfully printed.
                        # In this case, break out of this loop and log for the next `job_run_id`
                        break

    def retrieve_output(
        self, job_name: Optional[str] = None, job_id: Optional[str] = None,
    ) -> None:
        if not job_id:
            job = self._resolve_job_object(job_id, job_name)
            job_id = job.id

        try:
            output = self.api_client.find_structured_job_output_api_v2_structured_outputs_ha_job_output_ha_job_id_get(
                ha_job_id=job_id
            )
            self.log.log(json.dumps(output.result.output, indent=2))
        except Exception as e:  # noqa: BLE001
            traceback.print_exc()
            # Swallow if pretty print logic fails
            with contextlib.suppress(Exception):
                j = json.loads(e.body)  # type: ignore
                detail = j.get("error", {}).get("detail")
                self.log.error(detail)

    def _generate_random_job_name(self) -> str:
        """Generates a random job name
        Format:
            cli-job-{10 random characters}
        """
        random_chars = "".join(random.choices(string.ascii_letters, k=10)).lower()
        return "cli-job-" + random_chars

    def _get_all_job_runs(self, job_id: str) -> List[Job]:
        """Returns all job runs for a given job id.
        Returned in ascending order by creation time."""
        job_runs: List[Job] = search_entities(
            self.anyscale_api_client.search_jobs,
            JobsQuery(
                ha_job_id=job_id,
                show_ray_client_runs_only=False,
                sort_by_clauses=[
                    SortByClauseJobsSortField(
                        sort_field=JobsSortField.CREATED_AT, sort_order=SortOrder.ASC,
                    )
                ],
                paging=PageQuery(),
            ),
        )
        return job_runs
