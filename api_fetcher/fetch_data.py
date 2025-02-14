import json

import aiohttp
import asyncio

from api_fetcher.exceptions import (
    APITimeoutError,
    APIConnectionError,
    APIResponseError,
    APIDataError,
)


JSONPLACEHOLDER_URL = "https://jsonplaceholder.typicode.com/posts"


async def get_posts(session: aiohttp.ClientSession) -> list[dict]:
    try:
        async with session.get(JSONPLACEHOLDER_URL) as response:
            if response.status == 200:
                try:
                    json_response = await response.json()

                    return json_response
                except json.JSONDecodeError:
                    raise APIDataError()

            raise APIResponseError(status_code=response.status)
    except aiohttp.ClientConnectionError:
        raise APIConnectionError()
    except asyncio.TimeoutError:
        raise APITimeoutError()


async def main():
    async with aiohttp.ClientSession() as session:
        posts = await get_posts(session)


if __name__ == "__main__":
    asyncio.run(main())
