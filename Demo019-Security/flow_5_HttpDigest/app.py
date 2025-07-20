from fastapi import APIRouter, Depends, FastAPI, security, Security
from typing import Annotated

import json


router = APIRouter()

httpDigest = security.HTTPDigest()


async def getUser(
    credentials: Annotated[
        security.HTTPAuthorizationCredentials, Depends(httpDigest)
    ],
):
    return json.dumps(
        {
            'client credentials': {
                'credentials': credentials.credentials,
                'scheme': credentials.scheme,
            }
        }
    )


@router.get('/v5/viewUser')
async def apiSecurityCookie_scheme(
    usr_cred: Annotated[str, Depends(getUser)],
):
    return {'about': 'HTTPDigest', 'cred': usr_cred}
