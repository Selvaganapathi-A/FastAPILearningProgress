from httpx import AsyncClient, QueryParams

import asyncio
import hashlib
import string

from django.utils.crypto import get_random_string


async def generate():
    code_verifier = get_random_string(
        93, allowed_chars=string.ascii_letters + string.digits
    )
    code_challenge = hashlib.sha256(code_verifier.encode())
    state = get_random_string(
        43, allowed_chars=string.ascii_letters + string.digits
    )
    return state, code_verifier, code_challenge.hexdigest()


async def main():
    client = AsyncClient(
        max_redirects=5,
        follow_redirects=True,
        http2=True,
    )
    state, code_verifier, code_challenge = await generate()
    #
    print(state)
    print(code_verifier)
    print(code_challenge)
    #
    authorization_server = r'http://127.0.0.1:4000/authorize'
    params = QueryParams(
        {
            'response_type': 'code',
            'state': state,
            'client_id': '812_6DZeISZieLf0kumBdhW-',
            'client_secret': 'tq7Ecg05ic1Y-pCn2__MJmN1PjgW3_UwasZa831Ntku_EbIi',
            'redirect_url': 'http://127.0.0.1:4040/token',
            'scope': 'profile email dateofbirth'.split(' '),
            'code_challenge_method': 'S256',
            'code_challenge': code_challenge,
        }
    )
    #
    print('Query Params :', params, sep='\n')
    try:
        await client.get(authorization_server, params=params)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    asyncio.run(main=main())
    pass
