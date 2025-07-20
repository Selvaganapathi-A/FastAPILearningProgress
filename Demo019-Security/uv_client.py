from _uv_client import setup, show_response
from httpx import AsyncClient, QueryParams, Response

import asyncio
import orjson


async def main():
    client: AsyncClient = setup()
    #

    response: Response = await client.get(
        '/api/demo/apiKey/c',
        cookies={
            'SecretKey': 'fake-key-HongKong',
        },
    )
    await show_response(response)
    #
    response: Response = await client.get(
        '/api/demo/apiKey/h',
        headers={
            'SecretKey': 'London',
        },
    )
    await show_response(response)
    #
    response: Response = await client.get(
        '/api/demo/apiKey/q',
        params=QueryParams({'SecretKey': 'York Old'}),
    )
    await show_response(response)
    #
    # * OAuth Password Bearer
    response: Response = await client.post(
        '/api/demo/OAuth2/token',
        data={
            'client_id': '123',
            'client_secret': '456',
            'username': 'Jessica',
            'password': 'jessica@alba.1999',
            'grant_type': 'password',
            'scope': 'task:read task:write task:delete',
        },
    )
    token = orjson.loads(response.content).get('token', 'no token')
    print(token)
    await show_response(response)
    #
    response: Response = await client.get(
        '/birds',
        headers={
            'Authorization': 'Bearer ' + token,
        },
    )
    await show_response(response)
    # * HTTPDigest
    """
    Client must send Header like
        { 'Authorization': 'digest deadbeef12346' }
    """
    response: Response = await client.get(
        '/api/demo/HttpDigest/v5/viewUser',
        headers={'Authorization': 'digest deadbeef12346'},
    )
    await show_response(response)
    #
    # * HTTPBearer
    """
    Client must send Header like
        { 'Authorization': 'bearer deadbeef12346' }
    """

    response: Response = await client.get(
        '/api/demo/HttpBearer/v6/viewUser',
        headers={'Authorization': 'Bearer deadbeef12346'},
    )
    await show_response(response)
    #
    # * OAuth2 Auth Bearer
    response: Response = await client.post(
        '/api/demo/OAuth2Bearer/token',
        data={
            'client_id': 'xyz',
            'client_secret': 'abc',
            'username': 'Moana',
            'password': 'moana@azar.2002',
            'grant_type': 'password',
            'scope': 'linda jesse bianka',
        },
    )
    token = orjson.loads(response.content).get('token', 'no token')
    print(token)
    await show_response(response)
    #
    response: Response = await client.get(
        '/api/demo/OAuth2Bearer/goose',
        headers={
            'Authorization': 'Bearder ' + token,
        },
    )
    await show_response(response)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main=main())
