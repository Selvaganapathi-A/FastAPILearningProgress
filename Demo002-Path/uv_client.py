from _uv_client import setup, show_response
from colorama import Fore
from httpx import AsyncClient, Request, Response
from pprint import pprint

import orjson


async def main():
    client: AsyncClient = setup()

    #
    response: Response = await client.get('/items/45')
    await show_response(response)
    #
    response: Response = await client.get('/files/google.txt')
    await show_response(response)
    #
    response: Response = await client.get('/images/tango.png')
    await show_response(response)
    #
    response: Response = await client.get('/devices/nokia')
    await show_response(response)
    #
    response: Response = await client.get('/devices/blackberry')
    await show_response(response)
    #
    response: Response = await client.get('/devices/microsoft')
    await show_response(response)
    #
    response: Response = await client.get('/devices/redmi')
    await show_response(response)
    #
    response: Response = await client.get('/devices/nothing')
    await show_response(response)
    #
    response: Response = await client.get('/devices/i-phone')
    await show_response(response)
    #
    response: Response = await client.get('/product/45')
    await show_response(response)
    #
    response: Response = await client.get('/product/145')
    await show_response(response)
    #
    response: Response = await client.get('/product/459')
    await show_response(response)
    #
    response: Response = await client.get('/product/633')
    await show_response(response)
    #
    response: Response = await client.get('/product/845')
    await show_response(response)
    #
    response: Response = await client.get('/product/2011')
    await show_response(response)
    #


if __name__ == '__main__':
    import asyncio

    asyncio.run(main=main())
