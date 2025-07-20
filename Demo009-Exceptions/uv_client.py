from _uv_client import setup, show_response
from httpx import AsyncClient, QueryParams, Response

import orjson


async def main():
    client: AsyncClient = setup()
    #
    response: Response = await client.get('/api/v1/a/27')
    await show_response(response)
    #
    response: Response = await client.get('/api/v1/a/0')
    await show_response(response)
    #
    response: Response = await client.get('/api/v1/a/207')
    await show_response(response)
    #
    response: Response = await client.get('/api/v1/b/thorag')
    await show_response(response)
    #
    response: Response = await client.get('/api/v1/b/kid')
    await show_response(response)
    #
    response: Response = await client.get('/api/v1/b/president')
    await show_response(response)
    #
    response: Response = await client.get('/api/v1/c/anana')
    await show_response(response)
    #
    response: Response = await client.get('/api/v1/d/anana')
    await show_response(response)
    #


if __name__ == '__main__':
    import asyncio

    asyncio.run(main=main())
