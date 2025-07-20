from fastapi import exception_handlers, FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException


app: FastAPI = FastAPI()


@app.get('/api/v1/a/{item_id}')
async def v1a(item_id: int):
    if 0 < item_id < 100:
        return {'status': 'Success'}

    # ! Raising Exception
    raise HTTPException(
        status_code=404,
        detail='item id not in range(0 < 100)',
        # * Custom Header Message
        headers={
            'X-Error': 'Item ID not in range(0<100)',
        },
    )


""" Custom Exception Handler """


# * Define Exception class
class VarientError(Exception):
    def __init__(self, name: str, *args: object) -> None:
        self.name: str = name
        super().__init__(*args)


# * Register Exception with app
@app.exception_handler(VarientError)
async def varient_exception_handler(
    request: Request, exception: VarientError
):
    return JSONResponse(
        {
            'error': f'{exception.name} is in the wanted list. Avoid at all costs.'
        },
        status_code=451,
    )


bad_lokis = [
    'savage',
    'president',
    'japanese',
    'boastful',
]
good_lokis = ['kid', 'classic', 'aligator', '616', 'sylvie']


@app.get('/api/v1/b/{name}')
async def find_loki(name: str):
    if name in good_lokis:
        return {'status': 'you can trust them', 'name': name}
    elif name in bad_lokis:
        raise VarientError(name)
    else:
        return {'status': 'new varient. not in my watch', 'name': name}


""" Override Default Exception Handlers """


"""python

@app.exception_handler(exceptions.RequestValidationError)
async def override_requestvalidationerror(
    request: Request, exception: exceptions.RequestValidationError
):
    # * Returning PlainText Response instead of `Default RequestValidationError`
    return PlainTextResponse('Unable to Validate.', status_code=499)
    # return JSONResponse(
    #     content={
    #         'raised by': 'FastAPI - Internal Validation Mechanism',
    #         'message': 'Unable to Validate',
    #         'errors': exception.errors(),
    #         'body': exception.body,
    #     },
    #     status_code=422,
    # )

"""


@app.get('/api/v1/c/{item_id}')
async def v1c(item_id: int):
    return {'message': item_id}


""" Reuse Exception

If you want to use the exception along with the same default exception
handlers from FastAPI, you can import and reuse the default exception
handlers from fastapi.exception_handlers:

below demonstrate log the error message in console while using the same exception.

Itercept the error processing mechanism for logging and other such purposes.

"""


@app.exception_handler(HTTPException)
async def reuse_http_exception(request: Request, exception: HTTPException):
    # loggnig the error message while allowing existing error mechanism to work.
    print(exception.detail)
    return await exception_handlers.http_exception_handler(request, exception)


@app.get('/api/v1/d/{item_id}')
async def v1d(item_id: int):
    return {'message': item_id}
