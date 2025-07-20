from _uv_client import setup, show_response
from httpx import AsyncClient, QueryParams, Response

import orjson


async def main():
    # ! Any doubts
    client: AsyncClient = setup()
    #
    response: Response = await client.post(
        '/api/v1/login',
        data={
            'email': 'test@test.test',
            'token': (
                'Bearer xecRFpRMc9cGmyxcpC2hiFsasX2FiQ5WCX2Vo4aaeKbHID7BKstRzE6hz0cpZkzg'
            ),
        },
    )
    await show_response(response)
    #
    response: Response = await client.post(
        '/api/v2/login',
        data={
            'email': 'test+ghost@tango.cor',
            'password': 'FsasX2FiQ5WCX2Vo4',
        },
    )
    await show_response(response)
    #


if __name__ == '__main__':
    import asyncio

    from django.utils.crypto import get_random_string

    print(get_random_string(64))

    asyncio.run(main=main())
