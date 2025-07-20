from _uv_client import setup, show_response
from httpx import AsyncClient, Response


async def main():
    client: AsyncClient = setup()
    #
    response: Response = await client.get('')
    await show_response(response)
    #
    response: Response = await client.post('')
    await show_response(response)
    #
    response: Response = await client.put('')
    await show_response(response)
    #
    response: Response = await client.delete('')
    await show_response(response)
    #
    response: Response = await client.patch('')
    await show_response(response)
    #
    response: Response = await client.options('')
    await show_response(response)
    #
    response: Response = await client.head('')
    await show_response(response)
    #


if __name__ == '__main__':
    import asyncio

    asyncio.run(main=main())
