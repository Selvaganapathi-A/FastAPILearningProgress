from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from typing import Annotated, Any, Final

import datetime
import json
import jwt
import logging
import passlib
import passlib.context
import passlib.hash


APP_SECURITY_SCHEME = OAuth2PasswordBearer(
    tokenUrl='/api/security/token',
    scopes={
        'admin': 'what admin can do?',
        'manager': 'what admin can do?',
        'superviser': 'what admin can do?',
        'labor': 'what admin can do? only obey orders!😠',
    },
)
APP_SECRET_KEY: Final[str] = '0123456789-abcdefghijklmnopqrstuvwxyz'
APP_ALGORITHM: Final[str] = 'HS256'
#


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


async def get_username(
    security_scopes: SecurityScopes,
    token: Annotated[str, Depends(APP_SECURITY_SCHEME)],
):
    client_permission_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Not Enough Permissions',
        headers={'WWW-AUTHENDICATE': security_scopes.scope_str},
    )

    client_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid Token',
        headers={'WWW-AUTHENDICATE': security_scopes.scope_str},
    )

    data = await decode_token(token, onerror=client_exception)
    user_scopes = data.get('scopes', [])
    for scope in security_scopes.scopes:
        if scope not in user_scopes:
            raise client_permission_error

    print('Payload Data          :', data)
    print('Security Scopes       :', security_scopes.scopes)
    print('Security Scope String :', security_scopes.scope_str)

    return data['username']
