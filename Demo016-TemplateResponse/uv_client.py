from _uv_client import setup, show_response
from httpx import AsyncClient, QueryParams, Response

import orjson


async def main():
    client: AsyncClient = setup()
    #
    response: Response = await client.get('/api')
    await show_response(response)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main=main())
