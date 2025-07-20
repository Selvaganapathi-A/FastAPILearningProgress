from _uv_client import setup, show_response
from collections.abc import Iterable
from httpx import AsyncClient, QueryParams, Response

import orjson


async def main():
    client: AsyncClient = setup()
    #
    responses: Iterable[Response] = await asyncio.gather(
        client.get('/api'),
        client.get('/api?work=mop'),
        client.get('/api?work=wash car'),
        client.get('/api?work=bathe dog'),
        client.get('/api?work=clean utensils'),
        client.get('/api?work=return books'),
        client.get('/api?work=visit in-laws'),
        client.get('/api?work=holiday trip'),
    )

    for resp in responses:
        await show_response(resp)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main=main())
