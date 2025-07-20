from _uv_client import setup, show_response
from httpx import AsyncClient, QueryParams, Response

import orjson


async def main():
    client: AsyncClient = setup()
    #
    response: Response = await client.post(
        '/auth/login', data={'username': 'TestUser', 'password': 'TestPassword'}
    )
    await show_response(response)
    #
    response: Response = await client.post(
        '/auth/v2/login',
        headers={'token': '123-456-7809'},
    )
    await show_response(response)
    #
    response: Response = await client.post(
        '/auth/signup',
        data={
            'firstname': 'Test',
            'lastname': 'User',
            'email': 'test@test.test',
            'username': 'test@mnb',
            'password': 'test@password',
        },
    )
    await show_response(response)
    #
    response: Response = await client.get('/items/')
    await show_response(response)
    #
    response: Response = await client.get('/items/45')
    await show_response(response)
    #
    response: Response = await client.post(
        '/items/', content=orjson.dumps('Hello')
    )
    await show_response(response)
    #
    response: Response = await client.put(
        '/items/63', content=orjson.dumps('Hi')
    )
    await show_response(response)
    #
    response: Response = await client.patch(
        '/items/63', content=orjson.dumps('Junior')
    )
    await show_response(response)
    #
    response: Response = await client.delete('/items/72')
    await show_response(response)
    #


if __name__ == '__main__':
    import asyncio

    asyncio.run(main=main())
