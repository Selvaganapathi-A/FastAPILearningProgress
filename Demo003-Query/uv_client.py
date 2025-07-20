from _uv_client import setup, show_response
from httpx import AsyncClient, QueryParams, Response


async def main():
    client: AsyncClient = setup()
    #
    #

    response: Response = await client.get(
        '/books',
        params=QueryParams(
            {'start': 45},
        ),
    )
    await show_response(response)
    #
    response: Response = await client.get(
        '/books',
        params=QueryParams(
            {'start': 60, 'end': 90},
        ),
    )
    await show_response(response)
    #
    response: Response = await client.get(
        '/books',
        params=QueryParams(
            {'end': 45},
        ),
    )
    await show_response(response)
    #
    response: Response = await client.get(
        '/read',
        params=QueryParams(
            {'book_id': 1209},
        ),
    )
    await show_response(response)
    #
    response: Response = await client.get(
        '/read',
        params=QueryParams(
            {'book_id': 1209, 'author': 'lorenzo'},
        ),
    )
    await show_response(response)
    #
    response: Response = await client.get(
        '/read',
        params=QueryParams(
            {'book_id': 1209, 'author': 'lorenzo', 'exclude_old': 'on'},
        ),
    )
    await show_response(response)
    #
    response: Response = await client.get(
        '/read',
        params=QueryParams(
            {'book_id': 1209, 'author': 'lorenzo', 'exclude_old': 'yes'},
        ),
    )
    await show_response(response)
    #
    response: Response = await client.get(
        '/read',
        params=QueryParams(
            {'book_id': 1209, 'exclude_old': 'no'},
        ),
    )
    await show_response(response)
    #
    response: Response = await client.get(
        '/read',
        params=QueryParams(
            {'book_id': 1209, 'author': 'lorenzo', 'exclude_old': 0},
        ),
    )
    await show_response(response)
    #
    response: Response = await client.get(
        '/update',
        params=QueryParams(
            {'book_id': [1209, 1, 3, 5, 7, 9, 8, 13, 19]},
        ),
    )
    await show_response(response)
    #
    response: Response = await client.get(
        '/update',
        params=QueryParams(
            {'book_id': []},
        ),
    )
    await show_response(response)
    #
    response: Response = await client.get('/text')
    await show_response(response)
    #
    response: Response = await client.get(
        '/text',
        params=QueryParams(
            {'query': '1jasmin'},
        ),
    )
    await show_response(response)
    #
    response: Response = await client.get(
        '/text',
        params=QueryParams(
            {'query': '1e143534'},
        ),
    )
    await show_response(response)
    #
    response: Response = await client.get(
        '/text',
        params=QueryParams(
            {'query': '11233'},
        ),
    )
    await show_response(response)
    #
    response: Response = await client.get(
        '/text/',
        params=QueryParams(
            {'query': '112335345345342434'},
        ),
    )
    await show_response(response)
    response: Response = await client.get(
        '/card/validate',
        params=QueryParams(
            {'credit card': '4121 0349 2386 2230'},
        ),
    )
    await show_response(response)
    #
    response: Response = await client.get(
        '/card/validate',
        params=QueryParams(
            {'credit card': '4121 0340 2329 2239'},
        ),
    )
    await show_response(response)
    #
    response: Response = await client.get(
        '/fruits',
        params=QueryParams(
            {'query': ['banana', 'guava', 'apple', 'berry']},
        ),
    )
    await show_response(response)
    #
    response: Response = await client.get(
        '/token',
        params=QueryParams(
            {'token': 'Bearer ABCDEFGHIJmonpqrstuv0131'},
        ),
    )
    await show_response(response)
    #
    response: Response = await client.get(
        '/token',
        params=QueryParams(
            {'token': 'Bearer MNOPUVWXQRSTabcd', 'encrypted': 'yes'},
        ),
    )
    await show_response(response)
    #
    #


if __name__ == '__main__':
    import asyncio

    asyncio.run(main=main())
