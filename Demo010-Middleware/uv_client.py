from _uv_client import setup, show_response
from httpx import AsyncClient, QueryParams, Response

import orjson


async def main():
    client: AsyncClient = setup()
    #
    response: Response = await client.get('/api/v1')
    await show_response(response)
    #
    response: Response = await client.get(
        '/api/v1', headers={'Authorization': '123'}
    )
    await show_response(response)
    #
    # await asyncio.gather(*[client.get('/api/v1') for _ in range(1000)])
    #


if __name__ == '__main__':
    import asyncio

    asyncio.run(main=main())
