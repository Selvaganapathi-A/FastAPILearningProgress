from colorama import Back, Fore
from httpx import AsyncClient, Limits, QueryParams, Response, Timeout
from pprint import pprint

import orjson


def get_theme(status_code: int) -> tuple[str, str, str]:
    if 100 <= status_code < 199:
        return (
            Fore.GREEN + Back.BLACK,
            Fore.BLACK + Back.GREEN,
            Fore.RESET + Back.RESET,
        )

    elif 200 <= status_code < 299:
        return (
            Fore.BLUE + Back.BLACK,
            Fore.BLACK + Back.BLUE,
            Fore.RESET + Back.RESET,
        )

    elif 300 <= status_code < 399:
        return (
            Fore.YELLOW + Back.BLACK,
            Fore.BLACK + Back.YELLOW,
            Fore.RESET + Back.RESET,
        )

    elif 400 <= status_code < 499:
        return (
            Fore.RED + Back.BLACK,
            Fore.WHITE + Back.RED,
            Fore.RESET + Back.RESET,
        )

    elif 500 <= status_code < 599:
        return (
            Fore.MAGENTA + Back.BLACK,
            Fore.WHITE + Back.MAGENTA,
            Fore.RESET + Back.RESET,
        )
    raise ValueError('Status Code is Not in Range 100-600')


async def show_response(response: Response):
    status_code = response.status_code
    text, title, reset = get_theme(status_code=status_code)
    print(
        title,
        (
            f'{response.request.method: >7} : '
            f'{status_code: 3d} : {response.url} '
        ).ljust(105),
        sep='',
        end=reset,
    )
    headers = response.headers
    if headers:
        print(title, 'HEADERS '.rjust(105), sep='', end=reset)
        print(text, sep='', end='')
        for key in headers:
            print(f'{key: >30} : {headers[key]}')
        print(reset, sep='', end='')
    cookies = response.cookies
    if cookies:
        print(title, 'COOKIES '.rjust(105), sep='', end=reset)
        print(text, sep='', end='')
        for key in cookies:
            print(f'{key: >30} : {cookies[key]}')
        print(reset, sep='', end='')
    content_type = headers.get('content-type', '')
    # print(rp.content)
    if response.content == b'':
        pass
    else:
        print(title, 'CONTENT '.rjust(105), sep='', end=reset)
        print(text, sep='', end='')
        if content_type == 'application/json':
            pprint(orjson.loads(response.content), indent=2, width=105)
        else:
            print(text, response.content.decode(), sep='', end=reset)
        print(reset, sep='', end='')
    print()


def setup() -> AsyncClient:
    client = AsyncClient(
        base_url='http://127.0.0.1:8000',
        timeout=Timeout(timeout=10, connect=5),
        max_redirects=15,
        follow_redirects=True,
        limits=Limits(
            max_connections=8,
            max_keepalive_connections=3,
            keepalive_expiry=30,
        ),
    )
    return client
