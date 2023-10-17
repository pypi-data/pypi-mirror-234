import asyncio
from typing import List, Optional, Tuple

from anyscale.api_utils.exceptions.log_retrieval_errors import (
    wrap_as_unsupported_log_retrieval_method_error,
    wrap_job_run_log_not_retrievable_on_active_cluster_error,
)
from anyscale.api_utils.job_util import _get_job_run_id
from anyscale.api_utils.logs_util import (
    _download_log_from_ray_json_response,
    _download_logs_concurrently,
    _remove_ansi_escape_sequences,
)
from anyscale.cli_logger import LogsLogger
from anyscale.client.openapi_client.api.default_api import DefaultApi
from anyscale.client.openapi_client.models.base_job_status import BaseJobStatus
from anyscale.controllers.logs_controller import DEFAULT_PARALLELISM
from anyscale.sdk.anyscale_client.api.default_api import DefaultApi as BaseApi
from anyscale.sdk.anyscale_client.models.log_download_result import LogDownloadResult


async def _get_logs_from_active_job_run(
    base_api: BaseApi,
    job_run_id: str,
    raise_connection_issue_as_cli_error: bool = False,
    remove_escape_chars: bool = True,
) -> str:
    """
    Retrieves logs directly from the cluster (assumed to be active) that the job run is on.

    Raises:
        ExpectedLogRetrievalError: Reasons include:
            a. If the cluster is running < Ray 2.0
            b. The Anyscale SDK/CLI client cannot directly connect to the cluster
                (due to VPN issues or high load on the cluster)
    """
    # 1. Get the Ray API URL where it can stream (ie. download from active Ray cluster) job logs.
    # Raises ExpectedLogRetrievalError on a.
    with wrap_as_unsupported_log_retrieval_method_error():
        job_logs_url: str = base_api.get_job_logs_stream(
            job_id=job_run_id
        ).result.http_url
    # 2. Call the Ray API URL and parse the logs from the JSON response
    # Raises ExpectedLogRetrievalError on b.
    with wrap_job_run_log_not_retrievable_on_active_cluster_error(
        job_run_id, raise_connection_issue_as_cli_error
    ):
        logs = await _download_log_from_ray_json_response(job_logs_url)
        if remove_escape_chars:
            logs = _remove_ansi_escape_sequences(logs)
    return logs


async def _get_logs_from_running_production_job(
    base_api: BaseApi, production_job_id: str, remove_escape_chars: bool = True,
) -> str:
    """
    Retrieves logs directly from the cluster (assumed to be active) that the **job** is on.

    This is done by determining the last job run of the job and calling
    `_get_logs_from_active_job_run()` above.

    Raises:
        NoJobRunError: If a job run hasn't been created yet.
        ExpectedLogRetrievalError: See `_get_logs_from_active_job_run`
    """
    last_job_run_id = _get_job_run_id(base_api, job_id=production_job_id)
    return await _get_logs_from_active_job_run(
        base_api, last_job_run_id, remove_escape_chars
    )


async def _get_job_logs_from_storage_bucket(
    base_api: BaseApi,
    *,
    job_id: Optional[str] = None,
    job_run_id: Optional[str] = None,
    parallelism: int = DEFAULT_PARALLELISM,
    remove_escape_chars: bool = True,
) -> str:
    """Retrieves logs directly from the storage bucket.
    Currently, this is supported only for AWS clouds (through S3)

    Args:
        parallelism (int, optional): Defaults to 10 (AWS S3's default `max_concurrent_requests` value)
            There is no documented upper limit. However, please set a reasonable value.
        remove_escape_chars (bool, optional): Removes ANSI escape sequences from the logs, which are
            commonly used to color terminal output. Defaults to True.

    Raises:
        NoJobRunError: If a job run hasn't been created yet.
        ExpectedLogRetrievalError: If the job is on a cloud that does not support log download
            (such as GCP), or using the existing Anyscale V1 implementation.
    """
    job_run_id = _get_job_run_id(base_api, job_id=job_id, job_run_id=job_run_id)

    with wrap_as_unsupported_log_retrieval_method_error():
        log_download_result: LogDownloadResult = base_api.get_job_logs_download(
            job_id=job_run_id, all_logs=True
        ).result

    all_log_chunk_urls: List[str] = [chunk.chunk_url for chunk in log_download_result.log_chunks]  # type: ignore
    logs = await _download_logs_concurrently(all_log_chunk_urls, parallelism)
    if remove_escape_chars:
        logs = _remove_ansi_escape_sequences(logs)
    return logs


_JOB_RUN_TERMINAL_STATES = {
    BaseJobStatus.SUCCEEDED,
    BaseJobStatus.STOPPED,
    BaseJobStatus.COMPLETED,
    BaseJobStatus.FAILED,
    BaseJobStatus.UNKNOWN,
}


async def _get_job_logs_from_storage_bucket_streaming(
    api: DefaultApi,
    log: LogsLogger,
    *,
    next_page_token: Optional[str] = None,
    job_run_id: Optional[str] = None,
    parallelism: int = DEFAULT_PARALLELISM,
    remove_escape_chars: bool = True,
    cluster_journal_events_start_line: int = 0,
) -> Tuple[str, Optional[str], int, bool]:
    """Retrieves logs directly from the storage bucket.
    Also fetches cluster journal logs and print them to stderr inline with job logs.

    Args:
        parallelism (int, optional): Defaults to 10 (AWS S3's default `max_concurrent_requests` value)
            There is no documented upper limit. However, please set a reasonable value.
        remove_escape_chars (bool, optional): Removes ANSI escape sequences from the logs, which are
            commonly used to color terminal output. Defaults to True.

    Returns (logs, next_page_token, cluster_journal_events_new_start_line, is_job_run_terminated):
        Returns the logs output and the next page token for fetching additional logs.
        cluster_journal_events_new_start_line is the new start line for fetching cluster journal events.
        is_job_run_terminated is True if the job run is terminated, False otherwise.

    Raises:
        NoJobRunError: If a job run hasn't been created yet.
        ExpectedLogRetrievalError: If the job is on a cloud that does not support log download
            (such as GCP), or using the existing Anyscale V1 implementation.
    """
    # First fetch both the job info and the log chunks in parallel

    job_run_thread = api.get_decorated_job_api_v2_decorated_jobs_job_id_get(
        job_id=job_run_id, async_req=True
    )

    log_download_result_thread = api.get_job_logs_download_v2_api_v2_logs_job_logs_download_v2_job_id_get(
        job_id=job_run_id, next_page_token=next_page_token, async_req=True
    )

    # Once job info is fetched, fetch the cluster journal events
    job_run = job_run_thread.get().result
    cluster_id = job_run.cluster.id

    cluster_journal_events_thread = api.get_startup_logs_api_v2_sessions_session_id_startup_logs_get(
        cluster_id,
        start_line=cluster_journal_events_start_line,
        end_line=10000000,
        async_req=True,
    )

    # Wait for the log chunks API and start downloading the chunks in parallel
    log_download_result: LogDownloadResult = log_download_result_thread.get().result
    all_log_chunk_urls: List[str] = [chunk.chunk_url for chunk in log_download_result.log_chunks]  # type: ignore
    logs_task = asyncio.create_task(
        _download_logs_concurrently(
            all_log_chunk_urls,
            parallelism,
            bearer_token=log_download_result.bearer_token,
        )
    )

    # Print out the cluster journal events
    cluster_journal_events = cluster_journal_events_thread.get().result
    lines = cluster_journal_events.lines.splitlines()
    new_cluster_journal_events_start_line = (
        cluster_journal_events.start_line + cluster_journal_events.num_lines
    )
    if cluster_journal_events_start_line == 0:
        # When fetching the inital cluster journal events, we will just show the latest 10 events
        # to avoid flooding the output with too many events. In particular, after a job is
        # already running.
        lines = lines[-10:]
    for line in lines:
        log.info(line)

    # Finally wait for all the log chunks to download and return all the logs
    logs = await logs_task
    if remove_escape_chars:
        logs = _remove_ansi_escape_sequences(logs)
    new_next_page_token = (
        log_download_result.next_page_token
        if len(log_download_result.log_chunks) > 0
        else next_page_token
    )
    return (
        logs,
        new_next_page_token,
        new_cluster_journal_events_start_line,
        job_run.status in _JOB_RUN_TERMINAL_STATES,
    )
