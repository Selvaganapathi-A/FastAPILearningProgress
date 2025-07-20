from fastapi import APIRouter, Cookie, Depends, FastAPI, Query, security
from fastapi.responses import RedirectResponse
from typing import Annotated


scheme = security.oauth2.OAuth2AuthorizationCodeBearer(
    authorizationUrl='http://127.0.0.1:4000/authorize',
    tokenUrl='http://127.0.0.1:4000/token',
    refreshUrl='http://127.0.0.1:4000/refresh',
)


app = FastAPI()


@app.get('/')
async def function():
    pass
