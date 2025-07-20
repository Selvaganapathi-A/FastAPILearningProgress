from fastapi import BackgroundTasks, Body, Cookie, Depends, FastAPI, File, Form
from fastapi import middleware, Path, Query, requests, responses, staticfiles
from fastapi import status, UploadFile
from fastapi.security.oauth2 import OAuth2PasswordBearer
from fastapi.security.oauth2 import OAuth2PasswordRequestForm, SecurityScopes
from fastapi.templating import Jinja2Templates
from jwcrypto import jwk, jwt
from typing import Annotated, Any

import datetime
import jinja2
import json
import pathlib


app: FastAPI = FastAPI()
app.mount(
    '/static',
    staticfiles.StaticFiles(
        directory=pathlib.Path(__file__).parent / 'static'
    ),
    name='static',
)

templates = Jinja2Templates(
    directory=pathlib.Path(__file__).parent / 'templates'
)


@app.get('/{item_id}/{token}')
async def get_root(item_id: str, token: str, request: requests.Request):
    return templates.TemplateResponse(
        request=request,
        name='index.html',
        context={
            'token': token.upper(),
            'item_id': item_id,
        },
    )
