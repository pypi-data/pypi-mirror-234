import asyncio
from http import HTTPStatus
from unittest.mock import Mock, patch

from aiohttp import ClientConnectionError
from asynctest import CoroutineMock
import pytest

from anyscale.api_utils import job_logs_util
from anyscale.api_utils.exceptions.log_retrieval_errors import (
    UnsupportedLogRetrievalMethodError,
)
from anyscale.api_utils.job_logs_util import (
    _get_job_logs_from_storage_bucket,
    _get_logs_from_active_job_run,
    _get_logs_from_running_production_job,
)
from anyscale.api_utils.job_util import _get_job_run_id
from anyscale.api_utils.logs_util import (
    _download_log_from_ray_json_response,
    _download_logs_concurrently,
)
from anyscale.controllers.logs_controller import DEFAULT_PARALLELISM
from anyscale.sdk.anyscale_client.api.default_api import DefaultApi as BaseApi
from tests.api_utils.conftest import get_mock_api_exception, get_mock_base_api


@pytest.mark.asyncio()
async def test_get_logs_from_active_job_run():
    mock_stream_url = "https://valid.ray.dashboard/logs"
    mock_log_stream = Mock(http_url=mock_stream_url)
    mock_base_api = get_mock_base_api(
        {BaseApi.get_job_logs_stream.__name__: Mock(result=mock_log_stream)}
    )
    mock_logs = "logs"
    job_run_id = "job_123"

    with patch.object(
        job_logs_util,
        _download_log_from_ray_json_response.__name__,
        CoroutineMock(return_value=mock_logs),
    ) as mock_download_log_from_ray_json_response:
        assert (
            await _get_logs_from_active_job_run(mock_base_api, job_run_id) == mock_logs
        )
    mock_base_api.get_job_logs_stream.assert_called_once_with(job_id=job_run_id)
    mock_download_log_from_ray_json_response.assert_awaited_once_with(mock_stream_url)


# Indirectly tests `wrap_as_unsupported_log_retrieval_method_error()`
@pytest.mark.asyncio()
async def test_get_logs_from_active_job_run_throws_exception_anyscale_api():
    # Test expected ApiException
    error_message = "Cluster is not active."
    mock_api_exception = get_mock_api_exception(HTTPStatus.BAD_REQUEST, error_message)
    mock_base_api = get_mock_base_api(
        {BaseApi.get_job_logs_stream.__name__: mock_api_exception}
    )
    job_run_id = "job_123"
    with pytest.raises(UnsupportedLogRetrievalMethodError, match=error_message):
        await _get_logs_from_active_job_run(mock_base_api, job_run_id)

    # Test unexpected ApiException
    mock_api_exception.status = HTTPStatus.NOT_FOUND
    mock_api_exception.body = "Not found"
    with pytest.raises(Exception, match="Not found"):
        await _get_logs_from_active_job_run(mock_base_api, job_run_id)


# Indirectly tests `wrap_job_run_log_not_retrievable_on_active_cluster_error()`
@pytest.mark.asyncio()
async def test_get_logs_from_active_job_run_throws_exception_ray_dashboard_api():
    mock_base_api = get_mock_base_api(
        {
            BaseApi.get_job_logs_stream.__name__: Mock(
                result=Mock(http_url="https://valid.ray.dashboard/logs")
            )
        }
    )
    job_run_id = "job_123"

    for exception_type in [ClientConnectionError, asyncio.TimeoutError]:
        with patch.object(
            job_logs_util,
            _download_log_from_ray_json_response.__name__,
            CoroutineMock(side_effect=exception_type),
        ), pytest.raises(
            exception_type,
            match="only supported if the Anyscale client \\(SDK / CLI\\) can reach the cluster",
        ):
            await _get_logs_from_active_job_run(mock_base_api, job_run_id)


@pytest.mark.asyncio()
async def test_get_job_logs_from_storage_bucket():
    job_run_id = "job_123"
    mock_base_api = get_mock_base_api(
        {
            BaseApi.get_job_logs_download.__name__: Mock(
                result=Mock(log_chunks=[Mock(chunk_url="url1"), Mock(chunk_url="url2")])
            )
        }
    )
    mock_get_job_run_id = Mock(return_value=job_run_id)
    mock_logs = "a\nb"
    mock_download_logs_concurrently = CoroutineMock(return_value=mock_logs)
    to_patch = {
        _get_job_run_id.__name__: mock_get_job_run_id,
        _download_logs_concurrently.__name__: mock_download_logs_concurrently,
    }
    with patch.multiple(job_logs_util, **to_patch):
        assert (
            await _get_job_logs_from_storage_bucket(
                mock_base_api, job_run_id=job_run_id
            )
            == "a\nb"
        )
    mock_get_job_run_id.assert_called_once_with(
        mock_base_api, job_id=None, job_run_id=job_run_id
    )
    mock_base_api.get_job_logs_download.assert_called_once_with(
        job_id=job_run_id, all_logs=True
    )
    mock_download_logs_concurrently.assert_awaited_once_with(
        ["url1", "url2"], DEFAULT_PARALLELISM
    )

    # Test error from Anyscale API
    mock_download_logs_concurrently.reset_mock()
    error_message = "Cannot download"
    mock_base_api.get_job_logs_download.side_effect = get_mock_api_exception(
        HTTPStatus.BAD_REQUEST, error_message
    )
    with patch.multiple(job_logs_util, **to_patch), pytest.raises(
        UnsupportedLogRetrievalMethodError, match=error_message
    ):
        await _get_job_logs_from_storage_bucket(mock_base_api, job_run_id=job_run_id)
    mock_download_logs_concurrently.assert_not_awaited()


@pytest.mark.asyncio()
async def test_get_logs_from_running_production_job():
    job_id = "prodjob_123"
    job_run_id = "job_123"
    mock_base_api = Mock()
    mock_get_job_run_id = Mock(return_value=job_run_id)
    mock_logs = "a\nb"
    mock_get_logs_from_active_job_run = CoroutineMock(return_value=mock_logs)
    to_patch = {
        _get_job_run_id.__name__: mock_get_job_run_id,
        _get_logs_from_active_job_run.__name__: mock_get_logs_from_active_job_run,
    }
    with patch.multiple(job_logs_util, **to_patch):
        assert (
            await _get_logs_from_running_production_job(mock_base_api, job_id)
            == mock_logs
        )
    mock_get_job_run_id.assert_called_once_with(mock_base_api, job_id=job_id)
    mock_get_logs_from_active_job_run.assert_awaited_once_with(
        mock_base_api, job_run_id, True
    )
