from fastapi import APIRouter, Depends, HTTPException, Security, security
from pprint import pformat, pprint
from typing import Annotated, Any, Final

import datetime
import json
import jwt
import logging


APP_SECRET_KEY: Final[str] = '0123456789-abcdefghijklmnopqrstuvwxyz'
APP_ALGORITHM: Final[str] = 'HS256'
#
APP_AUTHORIZATION_SCHEME = security.OAuth2AuthorizationCodeBearer(
    # *
    authorizationUrl='/token/authorize',
    # * the url get token
    tokenUrl='/token',
    # * url to refresh token
    refreshUrl='/token/refresh',
    # * Security Scheme Name - in OpenAPI docs
    scheme_name='OAuth2-Authorization-Code-Bearer',
    # * The OAuth2 scopes that would be required by the *path operations* that
    # *     use this dependency.
    scopes={
        'CEO': 'manage Everything',
        'manager': 'manage division',
        'superviser': 'manage day to day works',
        'teamlead': 'manage scheduled tasks',
        'developer': 'fulfill tasks',
    },
)

"""
http://127.0.0.1:8000/token/authorize?
response_type=code&
client_id=Hello&
redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Fdocs%2Foauth2-redirect&
state=U3VuIEp1biAyOSAyMDI1IDE5OjQyOjU2IEdNVCswNTMwIChJbmRpYSBTdGFuZGFyZCBUaW1lKQ%3D%3D
"""

router = APIRouter()


async def create_token(
    data: dict[Any, Any],
    /,
    *,
    expires: datetime.timedelta = datetime.timedelta(hours=8),
) -> str:
    subject = json.dumps(data)
    expire_time = int((datetime.datetime.now() + expires).timestamp())
    payload = {'sub': subject, 'exp': expire_time}
    return jwt.encode(payload, key=APP_SECRET_KEY, algorithm=APP_ALGORITHM)


async def decode_token(token: str, *, onerror: HTTPException):
    try:
        payload = jwt.decode(
            token,
            key=APP_SECRET_KEY,
            algorithms=APP_ALGORITHM,
        )
        subject = payload['sub']
        return json.loads(subject)
    except Exception as e:
        logging.exception(e)
        raise onerror


async def _getUser(
    token: Annotated[str, Depends(APP_AUTHORIZATION_SCHEME)],
    security_scopes: security.SecurityScopes,
):
    payload = await decode_token(
        token, onerror=HTTPException(status_code=503)
    )
    print(token)
    print(payload)
    print(security_scopes.scope_str)
    print(security_scopes.scopes)
    return payload


@router.post('/token')
async def login(
    form: Annotated[
        security.OAuth2PasswordRequestFormStrict,
        Depends(security.OAuth2PasswordRequestFormStrict),
    ],
):
    form_data = {
        'client_id': form.client_id,
        'client_secret': form.client_secret,
        'grant_type': form.grant_type,
        'scopes': form.scopes,
        'username': form.username,
        'password': form.password,
    }
    return {
        'token': await create_token(
            {'user_pid': form.username, 'scopes': form.scopes},
            expires=datetime.timedelta(hours=6),
        )
    }


@router.get('/goose')
async def apiSecurityOAuth2PasswordBearer(
    user: Annotated[str, Security(_getUser, scopes=['admin', 'guest'])],
):
    return {
        'route': '',
        'user': user,
    }
