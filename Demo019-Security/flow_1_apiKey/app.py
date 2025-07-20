from fastapi import APIRouter, Depends, HTTPException, security
from typing import Annotated


router = APIRouter()


cookie_scheme = security.APIKeyCookie(name='SecretKey')
header_scheme = security.APIKeyHeader(name='SecretKey')
query_scheme = security.APIKeyQuery(name='SecretKey', scheme_name='deer')


async def verify_SecretKey(secret_key: str):
    if secret_key.startswith('fake-key-'):
        return secret_key
    raise HTTPException(status_code=402)


async def verify_SecretKey_from_Cookie(
    secret_key: Annotated[str, Depends(cookie_scheme)],
):
    print(secret_key)
    return {'Key': await verify_SecretKey(secret_key)}


async def verify_SecretKey_from_Header(
    secret_key: Annotated[str, Depends(header_scheme)],
):
    return {'Key': secret_key}


async def verify_SecretKey_from_Query(
    secret_key: Annotated[str, Depends(query_scheme)],
):
    return {'Key': secret_key}


@router.get('/c')
async def protected_route_1(
    session: Annotated[str, Depends(verify_SecretKey_from_Cookie)],
):
    return {'message': session}


@router.get('/h')
async def protected_route_2(
    session: Annotated[str, Depends(verify_SecretKey_from_Header)],
):
    return {'message': session}


@router.get('/q')
async def protected_route_3(
    session: Annotated[str, Depends(verify_SecretKey_from_Query)],
):
    return {'message': session}
