from fastapi import APIRouter, Depends, FastAPI, security, Security
from typing import Annotated

import json


router = APIRouter()

httpBasic = security.HTTPBasic()


async def getUser(
    credentials: Annotated[security.HTTPBasicCredentials, Depends(httpBasic)],
):
    credentials.username
    credentials.password

    return json.dumps(
        {
            'client credentials': {
                'username': credentials.username,
                'password': credentials.password,
            }
        }
    )


"""
visit browser

with this page
browser will ask for credentials and send them in header.

"""


@router.get('/v4/viewUser')
async def apiSecurityCookie_scheme(
    usr_cred: Annotated[str, Depends(getUser)],
):
    return {'about': 'HTTPBasic', 'cred': usr_cred}
