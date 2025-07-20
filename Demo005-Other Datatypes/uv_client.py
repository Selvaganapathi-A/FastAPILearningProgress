from _uv_client import setup, show_response
from httpx import AsyncClient, QueryParams, Response

import orjson


async def main():
    client: AsyncClient = setup()
    #
    response: Response = await client.get(
        '/',
        params={
            'unique_id': '31323334-3132-3334-3132-333431323334',
            'created': '2025-05-10 21:59:41.260168',
            'modified': '2025-05-10',
            'last_access_time': '21:59:41.260168',
            'last_downtime': '4 days, 0:00:00',
            'image': b'skdfjskdjfhksdjf',
            'weight': '32.123',
        },
    )
    await show_response(response)
    #


if __name__ == '__main__':
    import asyncio

    asyncio.run(main=main())
