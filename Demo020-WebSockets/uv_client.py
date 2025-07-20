from _uv_client import setup, show_response
from httpx import _exceptions, AsyncClient, ConnectError, ConnectTimeout
from httpx import NetworkError, QueryParams, ReadError, RequestError, Response

import logging
import orjson


async def make_requests(client: AsyncClient):
    response: Response = await client.get('/api')
    await show_response(response)


async def main():
    client: AsyncClient = setup()
    #
    try:
        await make_requests(client)
    except ConnectError as connectError:
        logging.error(connectError)
    finally:
        await client.aclose()


if __name__ == '__main__':
    import asyncio
    logging.basicConfig(
        style='{', format='{levelname: >10s} - {message}'
    )

    asyncio.run(main=main())
