from _uv_client import setup, show_response
from httpx import AsyncClient, QueryParams, Response

import orjson


async def main():
    client: AsyncClient = setup()
    #
    users = [
        {
            'name': 'spider name',
            'secret_name': 'peter parkar',
            'age': 35,
        },
        {
            'name': 'green arrow',
            'secret_name': 'john jefferson',
            'age': 54,
        },
        {
            'name': 'tony stark',
            'secret_name': 'iron man',
            'age': 74,
        },
        {
            'name': 'mary jane',
            'secret_name': 'spider gwen',
            'age': 19,
        },
        {
            'name': 'red hood',
            'secret_name': 'john mathew',
            'age': 21,
        },
    ]
    for user in users:
        response: Response = await client.post(
            '/api/hero',
            content=orjson.dumps(user),
        )
        await show_response(response)
    #
    user = {
        'name': 'spider man',
        # 'secret_name': 'peter parkar',
        'age': 33,
    }
    response: Response = await client.patch(
        '/api/hero/1',
        content=orjson.dumps(user),
    )
    await show_response(response)
    #
    response: Response = await client.get(
        '/api/hero/1',
    )
    await show_response(response)
    response: Response = await client.get(
        '/api/hero?offset=0&limit=19',
    )
    await show_response(response)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main=main())
