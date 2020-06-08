from time import time as current_time
import asyncio
from aiohttp import ClientSession

LAST_REQUEST_TIME = current_time()
DEFAULT_WAIT_TIME = 1.
SAFE_GET_LOCK = asyncio.Lock()


async def fetch_html(url: str, session: ClientSession, **kwargs) -> str:
    resp = await safe_get(url, session, **kwargs)
    resp.raise_for_status()
    html = await resp.text()
    return html


async def safe_get(url, session, wait_time=DEFAULT_WAIT_TIME, **kwargs):
    global LAST_REQUEST_TIME, SAFE_GET_LOCK
    sleep_time = 0
    async with SAFE_GET_LOCK:
        if current_time() - LAST_REQUEST_TIME < wait_time:
            sleep_time = LAST_REQUEST_TIME + wait_time - current_time()

        LAST_REQUEST_TIME = LAST_REQUEST_TIME + wait_time

    if sleep_time > 0:
        await asyncio.sleep(sleep_time)

    return await session.request(method="GET", url=url, **kwargs)
