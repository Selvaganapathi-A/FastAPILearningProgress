from collections.abc import Awaitable, Callable
from fastapi import FastAPI, Request, Response, status
from fastapi.middleware import cors
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

import time


app: FastAPI = FastAPI()


# * Middleware as a function
@app.middleware('http')
async def TimeSpentonServer(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    start = time.perf_counter_ns()
    response = await call_next(request)
    end = time.perf_counter_ns()
    response.headers['X-Process-Time'] = f'{(end - start) / 1000: >8.3f} µs'
    return response


# * Middleware as a class
class UserAgentMiddleware:
    async def __call__(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        auth_header = request.headers.get('Authorization')
        print(auth_header)
        # * this checks for Authorization Header
        if auth_header is None:
            print(
                {'missing': 'Authorization Header'},
            )
            # return JSONResponse(
            #     status_code=status.HTTP_401_UNAUTHORIZED,
            #     content={'missing': 'Authorization Header'},
            #     headers={'Missing': 'Authorization Header.'},
            # )
        return await call_next(request)


UA_Middleware = UserAgentMiddleware()
# * Add middleware as Object
app.add_middleware(BaseHTTPMiddleware, UA_Middleware)
# * Adding a middleware function which is defined externally
# app.add_middleware(BaseHTTPMiddleware, TimeSpentonServer)

# ! CORS Middleware

"""
Cross Origin Resource Sharing - refers to the situations when a frontend running
in a browser has JavaScript code that communicates with a backend,
and the backend is in a different "origin" than the frontend

You can also specify whether your backend allows:

    Credentials (Authorization headers, Cookies, etc).
    Specific HTTP methods (POST, PUT) or all of them with the wildcard "*".
    Specific HTTP headers or all of them with the wildcard "*".

"""
"""
- allow_origins - A list of origins that should be permitted to make cross-origin requests.
- allow_origin_regex - A regex string to match against origins that should be permitted to
    make cross-origin requests. e.g. `'https://.*\\.example\.org'`.
- allow_methods - A list of HTTP methods that should be allowed for cross-origin requests.
    Defaults to ['GET']
- allow_headers - A list of HTTP request headers that should be supported for cross-origin
    requests. Defaults to []. You can use ['*'] to allow all headers.
    The Accept, Accept-Language, Content-Language and Content-Type headers are always allowed
    for simple CORS requests
- allow_credentials - Indicate that cookies should be supported for cross-origin requests.
    Defaults to False. Also, allow_origins cannot be set to ['*'] for credentials to be allowed,
    origins must be specified.
- expose_headers - Indicate any response headers that should be made accessible to the browser.
    Defaults to [].
- max_age - Sets a maximum time in seconds for browsers to cache CORS responses.
    Defaults to 600.

# CORS preflight requests

    These are any OPTIONS request with Origin and Access-Control-Request-Method headers.
    In this case the middleware will intercept the incoming request and respond with
    appropriate CORS headers, and either a 200 or 400 response for informational purposes.

# Simple requests
    Any request with an Origin header. In this case the middleware will pass the request
    through as normal, but will include appropriate CORS headers on the response.

"""
origins = [
    # 'http://localhost.tiangolo.com',
    # 'https://localhost.tiangolo.com',
    # 'https://www.example.com:443',
    # 'http://localhost',
    # 'http://localhost:8080',
    'http://127.0.0.1:8000',
    # 'http://127.0.0.1:3000',
    # * my react front end server
    'http://localhost:3000',
]

app.add_middleware(
    cors.CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
    max_age=39600,
)


@app.get('/api/v1')
async def v1():
    return {'status': 'Ok'}
