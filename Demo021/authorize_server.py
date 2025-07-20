from fastapi import APIRouter, Cookie, Depends, FastAPI, Query, requests
from fastapi import security
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import Annotated


app = FastAPI()


class AuthorizationResponse(BaseModel):
    authorization_code: str
    state: str


class AccessTokenResponse(BaseModel):
    accesstoken: str
    tokentype: str = 'Bearer'
    expires: int
    refreshtoken: str


@app.get('/authorize', response_model=AuthorizationResponse)
async def function(
    response_type: Annotated[str, Query],
    client_id: Annotated[str, Query],
    client_secret: Annotated[str, Query],
    redirect_uri: Annotated[str, Query],
    scope: Annotated[str, Query],
    code_challenge: Annotated[str, Query],
    code_challenge_method: Annotated[str, Query],
    state: Annotated[str, Query],
    request: requests.Request,
):
    return RedirectResponse(url=redirect_uri)


@app.get('/token', response_model=AccessTokenResponse)
async def token(
    grant_type: Annotated[str, Query],
    code_challenge: Annotated[str, Query],
    code_challenge_method: Annotated[str, Query],
    client_id: Annotated[str, Query],
    client_secret: Annotated[str, Query],
):
    return ''
