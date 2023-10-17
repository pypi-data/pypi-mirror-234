import asyncio
from contextlib import contextmanager
from http import HTTPStatus
import json
from typing import Generator, Optional

from aiohttp import ClientConnectionError
from anyscale_client.exceptions import ApiException
from click import ClickException


class ExpectedLogRetrievalError(Exception):
    pass


class UnsupportedLogRetrievalMethodError(ExpectedLogRetrievalError):
    pass


class LogRetrievalTimeoutError(ExpectedLogRetrievalError):
    pass


@contextmanager
def wrap_as_unsupported_log_retrieval_method_error() -> Generator[None, None, None]:
    """
    Transforms Anyscale's `ApiException` into an expected error type.
    Usually the SDK/CLI client can try the next retrieval method if raised.
    """
    try:
        yield
    except ApiException as e:
        raise UnsupportedLogRetrievalMethodError(
            _get_exception_message(e)
        ) if e.status == HTTPStatus.BAD_REQUEST else e


def _get_exception_message(e: ApiException) -> Optional[str]:
    "Retrieves the `detail` method from any Anyscale `ApiException`"
    return json.loads(e.body).get("error", {}).get("detail")


@contextmanager
def wrap_job_run_log_not_retrievable_on_active_cluster_error(
    job_run_id: str, raise_connection_issue_as_cli_error: bool = False
) -> Generator[None, None, None]:
    """Parses a readable message for connection errors. Transforms connection errors for CLI."""
    try:
        yield
    except (ClientConnectionError, asyncio.TimeoutError) as e:
        error_msg = (
            f'Retrieving logs while the job is running is only supported if the Anyscale client (SDK / CLI) can reach the cluster running the job "{job_run_id}".\n'
            "Check that you are calling this from the same VPN as the cluster, or if the cluster is unreachable because of high load."
        )
        if raise_connection_issue_as_cli_error:
            raise ClickException(error_msg)
        else:
            raise type(e)(error_msg)
