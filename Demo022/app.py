from collections.abc import Awaitable, Callable
from fastapi import Cookie, Depends, FastAPI, Request, Response
from fastapi.middleware import cors
from fastapi.responses import UJSONResponse
from typing import Annotated, Any

import asyncio
import datetime
import pytz
import time


app: FastAPI = FastAPI()

app.add_middleware(
    cors.CORSMiddleware,
    allow_origins=('http://localhost:3000',),
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
    max_age=39600,
)
TIMEZONE = pytz.timezone('Asia/Calcutta')


@app.middleware('http')
async def middleware(
    req: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    print('client  :', req.client)
    print('headers :', req.headers)
    print('cookies :', req.cookies)
    p = time.perf_counter_ns()
    res = await call_next(req)
    q = time.perf_counter_ns()
    pt = q - p
    print(f'{pt / 1_000_000:.2f}')
    res.headers.append('X-Process-Time', f'{pt / 1_000_000:.2f} ms')
    return res


@app.get('/')
async def function(
    response: Response, visited: Annotated[int | None, Cookie()] = None
):
    global TIMEZONE
    previous_visits = visited
    if previous_visits is not None:
        previous_visits = previous_visits + 1
    else:
        previous_visits = 1
    # await asyncio.sleep(2.24)
    response = UJSONResponse(
        {
            'message': 'Hello',
            'generated': datetime.datetime.now(TIMEZONE).isoformat(),
            'visits': previous_visits,
        }
    )
    response.set_cookie(
        'visited',
        f'{previous_visits}',
        samesite='none',
        secure=True,
        httponly=True,
    )
    return response
