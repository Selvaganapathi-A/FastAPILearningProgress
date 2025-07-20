from fastapi import APIRouter, Depends, FastAPI, security, Security
from typing import Annotated

import json


router = APIRouter()

httpBearer = security.HTTPBearer()


async def getUser(
    bearer: Annotated[
        security.HTTPAuthorizationCredentials, Depends(httpBearer)
    ],
) -> str:
    return json.dumps(
        {
            'Bearer credentials': {
                'scheme': bearer.scheme,
                'credentials': bearer.credentials,
            }
        }
    )


@router.get('/v6/viewUser')
async def apiSecurityCookie_scheme(
    usr_cred: Annotated[str, Depends(getUser)],
):
    return {'about': 'HTTPBearer', 'cred': usr_cred}
