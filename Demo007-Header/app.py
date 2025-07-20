from fastapi import FastAPI, Header, Response, status
from typing import Annotated

import api_models
import datetime


app: FastAPI = FastAPI()


""" Headers
    - case insensitive
    - convert underscores with hypen on incoming vice versa
    - proxies may discard headers that are underscored instead of hypen
    - not seperated by space
    - if duplicate headers are sent first one takes priority unless it is captured by list or set
        header in fastapi

"""


@app.get('/api/v1/a')
async def v1a(
    # * Reading Headers
    accept: Annotated[str | None, Header()],
    accept_encoding: Annotated[str | None, Header()],
    priority: Annotated[str | None, Header()],
    x_api_token: Annotated[str, Header()],
    user_agent: Annotated[str | None, Header()] = None,
    tag: Annotated[list[str] | None, Header()] = None,
    X_Custom_Header: Annotated[
        str | None,
        Header(
            alias='Custom_Header',
            convert_underscores=False,
        ),
    ] = None,
):
    return {
        'Headers': {
            'accept': accept,
            'accept_encoding': accept_encoding,
            'priority': priority,
            'tags': tag,
            'user_agent': user_agent,
            'x_api_token': x_api_token,
            'X Custom Header': X_Custom_Header,
        }
    }


@app.get('/api/v1/b', status_code=status.HTTP_208_ALREADY_REPORTED)
async def wv1b(response: Response):
    # * set Headers
    response.headers['FastAPI-Generated-Header'] = (
        'FastAPI ' + datetime.datetime.now().isoformat()
    )
    return {}


@app.get('/api/v1/c')
async def v1c(
    model: Annotated[api_models.ModelBrowserRequestHeaders, Header()],
):
    return {'headers': model}
