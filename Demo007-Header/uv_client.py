from _uv_client import setup, show_response
from httpx import AsyncClient, QueryParams, Response

import orjson


async def main():
    client: AsyncClient = setup()
    #
    response: Response = await client.get(
        '/api/v1/a', headers={'priority': '6675', 'x-api-token': '5564'}
    )
    await show_response(response)
    #
    response: Response = await client.get(
        '/api/v1/a',
        headers=[
            ('priority', '6675'),
            ('x-api-token', '5564'),
            # * duplicate headers
            ('tag', 'movie'),
            ('tag', 'theatre'),
            ('tag', 'sound system'),
            # * valid headers
            ('Custom_Header', 'Lemouria Star Satelite'),
            ('custom_header', 'ISRO PSLV'),
            # ! invalid header
            ('custom-header', 'ISRO SLV'),
        ],
    )
    await show_response(response)
    #
    response: Response = await client.get('/api/v1/b', headers=[])
    await show_response(response)
    #
    response: Response = await client.get(
        '/api/v1/c',
        headers=[
            ('sec-gpc', '49'),
            ('sec-fetch-mode', 'lockheed'),
        ],
    )
    await show_response(response)
    #


if __name__ == '__main__':
    import asyncio

    asyncio.run(main=main())
