from api_models import UserIn, UserOut
from fastapi import FastAPI, responses, status

import random


app: FastAPI = FastAPI(
    # * this setting will use ORJSONResponse instead of default JSONResponse
    # We can still override this behaviour by `response_class` in Path Opertaions
    default_response_class=responses.ORJSONResponse,
)


@app.get(
    '/',
    # * Other Status Codes than the default FastAPI StatusCode
    status_code=status.HTTP_102_PROCESSING,
    # * Tags used to group paths together in docs [swagger, redoc, etc...]
    tags=['one', 'cow', 'clown', 'yarn'],
    summary='A summary about path',
    description='a brief about this path in docs',
)
async def function():
    return {'Message': 'Path Operation Documentationd'}


@app.get('/api/v2')
async def v2():
    """
    Any Markdown text placed here will be used for docs if description not provided.
    **Like** __this__
    [urltext](http://example.com/docs)
    """
    return {'Message': 'Path Operation Alt Documentationd'}


"""

Response Class
All other responses are inherited from this class

JSONResponse
HTMLResponse
ORJSONResponse
UJSONResponse
PlainTextResponse
RedirectResponse
StreamingResponse
FileResponse
"""


@app.get('/api/legacy')
async def api_legacy():
    content = """<?xml version="1.0"?>
    <shampoo>
    <Header>
        Apply shampoo here.
    </Header>
    <Body>
        You'll have to use soap here.
    </Body>
    <About>
        XML Response.
    </About>
    </shampoo>"""
    return responses.Response(
        content=content,
        status_code=290,
        headers={'Response-Type': 'XMLResponse'},
        media_type='text/xml; charset=utf-8;',
    )


@app.get('/api/v1/JSONResponse', response_class=responses.JSONResponse)
async def api_v1_jsonresponse():
    return responses.JSONResponse(
        {
            'method': 'GET',
            'response_class': 'JSONResponse',
        },
        headers={'About-Response': 'JSONResponse'},
    )


@app.get('/api/v1/HTMLResponse', response_class=responses.HTMLResponse)
async def api_v1_HTMLResponse():
    return responses.HTMLResponse(
        '<html><body><p>HTMLResponse</p></body></html>',
        headers={'About-Response': 'HTMLResponse'},
    )


@app.get('/api/v1/ORJSONResponse', response_class=responses.ORJSONResponse)
async def api_v1_ORJSONResponse():
    return responses.ORJSONResponse(
        {
            'method': 'GET',
            'response_class': 'ORJSONResponse',
        },
        headers={'About-Response': 'ORJSONResponse'},
    )


"""
pip install UJSON
"""


@app.get('/api/v1/UJSONResponse', response_class=responses.UJSONResponse)
async def api_v1_UJSONResponse():
    return responses.UJSONResponse(
        {
            'method': 'GET',
            'response_class': 'UJSONResponse',
        },
        headers={'About-Response': 'UJSONResponse'},
    )


@app.get(
    '/api/v1/PlainTextResponse', response_class=responses.PlainTextResponse
)
async def api_v1_PlainTextResponse():
    return responses.PlainTextResponse(
        """Plain Response Sent As Is""",
        headers={'About-Response': 'PlainTextResponse'},
    )


@app.get(
    '/api/v1/RedirectResponse', response_class=responses.RedirectResponse
)
async def api_v1_RedirectResponse():
    return responses.RedirectResponse(
        '/api/legacy',
        headers={
            'About-Response': 'Response',
        },
    )


async def generate_random_bytes():
    for _ in range(30):
        'Generate Some Video Bytes Here...'
        yield random.randbytes(4)


@app.get('/api/v1/StreamingResponse')
async def api_v1_StreamingResponse():
    return responses.StreamingResponse(
        generate_random_bytes(),
    )


def read_file_content():
    with open(
        'C:/Users/Tesla/Downloads/downloads/Jane Vinz/00.jpg', 'rb'
    ) as reader:
        yield from reader


@app.get('/api/v1/StreamingResponse/file')
async def api_v1_StreamingResponse_file():
    return responses.StreamingResponse(read_file_content())


""" Response Model """


@app.put(
    '/api/v6/users/{user_id}',
    # ! Using different model for output prevents leakage like sensitve passwords etc
    response_model=UserOut,
    # * if anyy field is none they are not included in response
    response_model_exclude_none=True,
    # * if value is not set for any of those model fields are excluded
    response_model_exclude_unset=True,
    # * fields with default values are also excluded
    response_model_exclude_defaults=True,
    # * specified fields are not sent to client like passwords
    response_model_exclude={'email'},
    response_model_by_alias=True,
)
async def api_v6_users(user: UserIn, user_id: int):
    print(user_id)
    return user
