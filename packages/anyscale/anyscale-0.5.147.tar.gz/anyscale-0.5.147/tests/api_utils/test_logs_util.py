from unittest.mock import Mock, patch

from aiohttp import ClientSession, WSMsgType
from asynctest import CoroutineMock
import pytest

from anyscale.api_utils import logs_util
from anyscale.api_utils.logs_util import (
    _download_log_from_s3_url,
    _remove_ansi_escape_sequences,
    _stream_log_from_ray_websocket,
)
from anyscale.shared_anyscale_utils.test_util import MockAsyncContextManagerReturnValue


# Indirectly tests gather_in_batches()
@pytest.mark.asyncio()
async def test_download_logs_concurrently():
    # Test all downloads succeed
    with patch.object(
        logs_util,
        _download_log_from_s3_url.__name__,
        CoroutineMock(side_effect=["logs_from_chunk_1\n", "logs_from_chunk_2"]),
    ) as mock_download_log_from_s3_url:
        result = await logs_util._download_logs_concurrently(
            ["http://presigned.url.1", "http://presigned.url.2"], 1
        )
    assert result == "logs_from_chunk_1\nlogs_from_chunk_2"
    assert mock_download_log_from_s3_url.call_count == 2

    # Test one download fail raise exception
    exception_msg = "Log chunk download failed"
    with patch.object(
        logs_util,
        _download_log_from_s3_url.__name__,
        CoroutineMock(side_effect=Exception(exception_msg)),
    ) as mock_download_log_from_s3_url, pytest.raises(Exception, match=exception_msg):
        result = await logs_util._download_logs_concurrently(
            ["http://presigned.url.1", "http://presigned.url.2"], 1
        )


@pytest.mark.asyncio()
async def test_stream_log_from_ray_websocket():
    mock_websocket = MockAsyncContextManagerReturnValue(
        receive=CoroutineMock(
            side_effect=[
                Mock(type=WSMsgType.TEXT, data="\n \x1b[1mABC "),
                Mock(type=WSMsgType.ERROR),
                Mock(type=WSMsgType.CLOSED),
            ]
        )
    )
    mock_url = "https://ray.websocket.url"
    mock_log_callback = Mock()
    # Test normal case, newlines and spaces are stripped,
    # and ANSI escape sequences are removed by default
    with patch.object(
        ClientSession, ClientSession.ws_connect.__name__, return_value=mock_websocket
    ) as mock_ws_connect:
        await _stream_log_from_ray_websocket(mock_url, mock_log_callback)
    # This is actually an `async def` fn, but is mocked as a normal `def` fn
    mock_ws_connect.assert_called_once_with(mock_url)
    assert mock_websocket.receive.call_count == 3
    mock_log_callback.assert_called_once_with("ABC")


def test_remove_ansi_escape_sequences():
    string_with_ansi_escape_sequences = "\x1b[1m\x1b[31mHello World\x1B[0m\x1B[0m"
    assert (
        _remove_ansi_escape_sequences(string_with_ansi_escape_sequences)
        == "Hello World"
    )
