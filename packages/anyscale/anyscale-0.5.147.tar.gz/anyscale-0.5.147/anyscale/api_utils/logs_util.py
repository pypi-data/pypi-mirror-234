import asyncio
import re
from typing import Any, Callable, List, Optional

import aiohttp
from aiohttp import WSMsgType

from anyscale.shared_anyscale_utils.utils.asyncio import gather_in_batches


CLUSTER_CONNECT_TIMEOUT = 30


async def _download_logs_concurrently(
    log_chunk_urls: List[str], parallelism: int, bearer_token: Optional[str] = None
) -> str:
    logs_across_chunks: List[str] = await gather_in_batches(  # type: ignore
        parallelism,
        *[
            _download_log_from_s3_url(url, bearer_token=bearer_token)
            for url in log_chunk_urls
        ],
    )
    logs_across_chunks = [log.strip() for log in logs_across_chunks]
    return "\n".join(logs_across_chunks)


async def _download_log_from_ray_json_response(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        response = await asyncio.wait_for(
            session.get(url), timeout=CLUSTER_CONNECT_TIMEOUT
        )
        logs: str = (await response.json()).get("logs", "")
        return logs


async def _download_log_from_s3_url(
    url: str, bearer_token: Optional[str] = None,
) -> str:
    # Note that the URL is presigned, so no token needs to be passed in the request
    async with aiohttp.ClientSession() as session:
        headers = {"Authorization": f"Bearer {bearer_token}"} if bearer_token else {}
        async with session.get(url, headers=headers) as response:
            return await response.text()


# For job logs, the implementation is same as
# https://github.com/ray-project/ray/blob/6142f52ada995b7123ea7347a70613ca7b924e0c/dashboard/modules/job/sdk.py#L426
# However Ray is only part of [all] install, so we replicate the functionality here.
async def _stream_log_from_ray_websocket(
    url: str, log_callback: Callable[[str], Any], remove_escape_chars: bool = True
) -> None:
    async with aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(total=CLUSTER_CONNECT_TIMEOUT)
    ) as session:
        async with session.ws_connect(url) as ws:
            while True:
                msg = await ws.receive()
                if msg.type == WSMsgType.TEXT:
                    logs = msg.data.strip()
                    if remove_escape_chars:
                        logs = _remove_ansi_escape_sequences(logs)
                    log_callback(logs)
                elif msg.type == WSMsgType.CLOSED:
                    break
                elif msg.type == WSMsgType.ERROR:
                    pass


def _remove_ansi_escape_sequences(s: str) -> str:
    # Required as the log may contain ANSI escape sequeneces (e.g. for coloring in the terminal)
    # Regex pattern from https://stackoverflow.com/a/14693789
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    return ansi_escape.sub("", s)
