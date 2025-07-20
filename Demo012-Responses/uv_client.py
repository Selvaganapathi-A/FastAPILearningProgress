from _uv_client import setup, show_response
from httpx import AsyncClient, QueryParams, Response

import orjson


async def main():
    client: AsyncClient = setup()
    #
    # response: Response = await client.get('/')
    # await show_response(response)
    #
    """
    response: Response = await client.get('/api/v2')
    await show_response(response)
    #
    response: Response = await client.get('/api/legacy')
    await show_response(response)
    #
    response: Response = await client.get('/api/v1/jsonresponse')
    await show_response(response)
    #
    response: Response = await client.get('/api/v1/HTMLResponse')
    await show_response(response)
    #
    response: Response = await client.get('/api/v1/ORJSONResponse')
    await show_response(response)
    #
    response: Response = await client.get('/api/v1/UJSONResponse')
    await show_response(response)
    #
    response: Response = await client.get('/api/v1/PlainTextResponse')
    await show_response(response)
    #
    response: Response = await client.get('/api/v1/RedirectResponse')
    await show_response(response)
    #
    response: Response = await client.get('/api/v1/StreamingResponse')
    print(response.headers)
    print(response.status_code)
    print('-' * 80)
    for content in response.iter_bytes(16):
        print('###', content)
    print('-' * 80)
    #
    response: Response = await client.get('/api/v1/StreamingResponse/file')
    print(response.headers)
    print(response.status_code)
    # print('-' * 80)
    # for content in response.iter_bytes(20):
    #     print(content)
    # print('-' * 80)
    #
    """
    response: Response = await client.put(
        '/api/v6/users/45',
        content=orjson.dumps(
            {
                'first_name': 'leo',
                'date_of_birth': '2009-12-31',
                'email': 'leo@google.bin',
                'password': 'tgbyhnujm',
            },
        ),
    )
    await show_response(response)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main=main())
