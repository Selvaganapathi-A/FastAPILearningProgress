from _uv_client import setup, show_response
from httpx import AsyncClient, QueryParams, Response

import orjson


async def main():
    client: AsyncClient = setup()
    #

    user = {
        'firstname': 'nala',
        'lastname': 'brooks',
        'email': 'nalabrookes@gmail.reddit',
        'dateofbirth': '2009-06-24',
        'province': 'Minnosotta',
        'country': 'London',
    }
    response: Response = await client.post('/user', content=orjson.dumps(user))
    await show_response(response)
    #
    user = {
        'firstname': 'tony',
        'lastname': 'stark',
        'email': 'tonystark@starkindustries.us',
        'dateofbirth': '2004-12-31',
        'state': 'Seattle',
        'province': 'Arizona',
        'country': 'United Arab Kingdom',
    }
    response: Response = await client.post('/user', content=orjson.dumps(user))
    await show_response(response)
    #
    response: Response = await client.put(
        '/user/23', content=orjson.dumps(user)
    )
    await show_response(response)
    #
    response: Response = await client.put(
        '/user/654', content=orjson.dumps(user)
    )
    await show_response(response)
    #
    response: Response = await client.put(
        '/user/23', params={'fake': True}, content=orjson.dumps(user)
    )
    await show_response(response)
    #
    response: Response = await client.put(
        '/user/23', params={'fake': 'off'}, content=orjson.dumps(user)
    )
    await show_response(response)
    #
    response: Response = await client.put(
        '/items/445',
        params={
            'rate_conversion': 'asia/specific',
        },
        content=orjson.dumps(
            {
                'product': {
                    'category': 'bakey',
                    'name': 'butter biscuit',
                    'price': 2,
                    'taxable': False,
                },
                'rating': 4,
            }
        ),
    )
    await show_response(response)
    #
    response: Response = await client.put(
        'api/v1/student/?joined=2015',
        content=orjson.dumps(
            {
                'student': {
                    'rollno': 54,
                    'name': 'keerthi',
                    'std': 'x',
                },
            }
        ),
    )
    #
    await show_response(response)
    response: Response = await client.put(
        'api/v2/student/',
        content=orjson.dumps(
            {
                'rollno': 16,
                'name': 'meenakshi',
                'std': 'ix',
            }
        ),
    )
    await show_response(response)
    #
    response: Response = await client.put(
        'api/v1/state',
        content=orjson.dumps(
            {
                'name': 'new york',
                'declared': 1999,
            }
        ),
    )
    await show_response(response)
    #
    response: Response = await client.put(
        'api/v1/state',
        content=orjson.dumps(
            {
                'name': 'queens',
                'declared': 1998,
                'tags': [
                    'factory',
                    'marvel',
                    'batman',
                    'falsh',
                    'arrow',
                    'kawk eye',
                    'crimes',
                ],
            }
        ),
    )
    await show_response(response)
    #
    response: Response = await client.put(
        'api/v1/state',
        content=orjson.dumps(
            {
                'name': 'queens',
                'declared': 1998,
                'province': [
                    {
                        'name': 'london',
                        'declared': 1698,
                    },
                    {
                        'name': 'sweden',
                        'declared': 1698,
                    },
                    {
                        'name': 'amsterdam',
                        'declared': 1898,
                    },
                ],
                'tags': [
                    'factory',
                    'marvel',
                    'batman',
                    'falsh',
                    'arrow',
                    'hawk eye',
                    'crimes',
                ],
            }
        ),
    )
    await show_response(response)

    response: Response = await client.post(
        'api/v1/product',
        content=orjson.dumps(
            {
                'category': 'spice',
                'name': 'chilli',
                'price': 1.2,
                'taxable': True,
            },
        ),
    )
    await show_response(response)
    response: Response = await client.post(
        'api/v1/product',
        content=orjson.dumps(
            {
                'category': 'nuts',
                'name': 'channa',
                'price': 0.8,
                'taxable': False,
            },
        ),
    )
    await show_response(response)
    #
    response: Response = await client.get('api/v1/product')
    await show_response(response)
    #
    await show_response(response)
    response: Response = await client.patch(
        'api/v1/product/chilli',
        content=orjson.dumps(
            {
                'price': 45.8,
            },
        ),
    )
    await show_response(response)
    #
    response: Response = await client.get('api/v1/product')
    await show_response(response)
    #
    response: Response = await client.get('api/v1/product/chilli')
    await show_response(response)
    #


if __name__ == '__main__':
    import asyncio

    asyncio.run(main=main())
