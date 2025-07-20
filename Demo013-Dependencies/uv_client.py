from _uv_client import setup, show_response
from httpx import AsyncClient, QueryParams, Response

import orjson


async def main():
    client: AsyncClient = setup()
    #
    response: Response = await client.get('/api/v1/a')
    await show_response(response)
    #
    response: Response = await client.get('/api/v1/b')
    await show_response(response)
    #
    response: Response = await client.get('/api/v1/b?app_version=903.345.2342')
    await show_response(response)
    #
    response: Response = await client.get('/api/v1/a?app_version=111.23.45')
    await show_response(response)
    #
    response: Response = await client.get('/api/v1/c')
    await show_response(response)
    #
    response: Response = await client.get(
        '/api/v1/d?brand=tata&model=vitara&price=6375499&app_version=0.112.45'
    )
    await show_response(response)
    #
    response: Response = await client.get(
        '/api/v1/e?brand=honda&model=activa&price=2275499&app_version=0.112.49'
    )
    await show_response(response)
    #
    response: Response = await client.get(
        '/api/v1/f',
        headers={
            'scope-expiry': '2022-12-31',
            'scopes': 'user:read admin:read,write',
        },
    )
    await show_response(response)
    #
    response: Response = await client.get(
        '/api/v1/f',
        headers={
            'scope-expiry': '2025-06-18',
            'scopes': 'user:read,write admin:read,write,execute third_party:read',
        },
    )
    await show_response(response)
    #
    response: Response = await client.get(
        '/api/v1/f',
        headers={
            'scope-expiry': '2024-06-19',
        },
    )
    await show_response(response)
    #
    response: Response = await client.get(
        '/api/v1/g',
        headers={
            'X-Access-token': '2024-06-19',
        },
    )
    await show_response(response)
    #
    response: Response = await client.get(
        '/api/v1/g',
        headers={
            'X-Access-token': 'fake-user-account-token',
        },
    )
    await show_response(response)
    #
    response: Response = await client.get(
        '/api/v1/a',
        headers={
            'super-secret-key': 'dummykey',
            'super-secret-token': 'dummytoken',
        },
    )
    await show_response(response)
    #


if __name__ == '__main__':
    import asyncio

    asyncio.run(main=main())
