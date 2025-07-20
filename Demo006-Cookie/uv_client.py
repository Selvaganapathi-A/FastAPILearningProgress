from _uv_client import setup, show_response
from httpx import AsyncClient, QueryParams, Response

import orjson


async def main():
    client: AsyncClient = setup()
    #
    response: Response = await client.get('/api/v/1/a/')
    await show_response(response)
    #
    response: Response = await client.get('/api/v/1/a/')
    await show_response(response)
    #
    response: Response = await client.get('/api/v/1/b/')
    await show_response(response)
    #
    response: Response = await client.get('/api/v/1/b/')
    await show_response(response)
    #
    response: Response = await client.get('/api/v/1/a/')
    await show_response(response)
    #
    response: Response = await client.get(
        '/api/v/1/c',
        cookies={
            'language': 'en-US',
            'ad_id': 'Hello',
            'click_id': '54',
        },
    )
    await show_response(response)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main=main())
