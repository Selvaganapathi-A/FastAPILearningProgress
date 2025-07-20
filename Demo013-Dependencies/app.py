from fastapi import Body, Depends, FastAPI, Form, Header, HTTPException, Query
from fastapi import status
from pydantic import AfterValidator
from typing import Annotated, Iterable, Never

import contextlib
import datetime
import random


@contextlib.asynccontextmanager
async def lifecycleManager(app: FastAPI):
    print('Code placed Here Will be executed before application starts.')
    yield
    # Cleanup codes
    print('Code placed Here Will be executed after exiting application.')


# * Global Dependency


async def verify_access_key(
    super_secret_key: Annotated[str | None, Header()] = None,
):
    # print(super_secret_key)
    # print(super_secret_key is None, super_secret_key != 'dummykey')
    # print(super_secret_key is None or super_secret_key != 'dummykey')
    if super_secret_key is None or super_secret_key != 'dummykey':
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)


async def verify_access_token(
    super_secret_token: Annotated[str | None, Header()] = None,
):
    # print(super_secret_token)
    # print(super_secret_token is None, super_secret_token != 'dummytoken')
    # print(super_secret_token is None or super_secret_token != 'dummytoken')
    if super_secret_token is None or super_secret_token != 'dummytoken':
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)


app: FastAPI = FastAPI(
    lifespan=lifecycleManager,
    redirect_slashes=True,
    # ! be cautious
    # ! These Dependencies run for every path operations
    dependencies=[
        Depends(verify_access_key),
        Depends(verify_access_token),
    ],
)


"""
"Dependency Injection" means, in programming, that there is a way for your code
(in this case, your path operation functions) to declare things that it requires
to work and use: "dependencies".

And then, that system (in this case FastAPI) will take care of doing whatever
is needed to provide your code with those needed dependencies
("inject" the dependencies).

This is very useful when you need to:

    Have shared logic (the same code logic again and again).
    Share database connections.
    Enforce security, authentication, role requirements, etc.
    And many other things...

All these, while minimizing code repetition.
"""


# * Common Dependency That get App Version From Query
async def get_app_version(
    app_version: Annotated[
        str | None,
        Query(
            pattern=r'^\d+\.\d+\.\d+$',
        ),
    ] = None,
):
    if app_version:
        return app_version
    else:
        return '0.0.0'


@app.get('/api/v1/a')
async def get_v1a(app_version: Annotated[str, Depends(get_app_version)]):
    return {
        'path': 'v1/a',
        'version': app_version,
    }


@app.get('/api/v1/b')
async def get_v1b(app_version: Annotated[str, Depends(get_app_version)]):
    return {
        'path': 'v1/b',
        'version': app_version,
    }


# * Dependency with yield
async def any_random_number():
    random_number: int = random.randint(1000, 9999)
    yield random_number
    del random_number


@app.get('/api/v1/c')
async def get_(
    # * dependency one
    app_version: Annotated[int, Depends(get_app_version)],
    # * dependency two
    random_number: Annotated[int, Depends(any_random_number)],
):
    return {
        'path': 'v1/c',
        'version': app_version,
        'user_count': random_number,
    }


# * Dependency as Class
class Car:
    def __init__(self, brand: str, model: str, price: int) -> None:
        self._brand: str = brand
        self._model: str = model
        self._price: float = price

    def info(self):
        return {
            'brand': self._brand,
            'model': self._model,
            'price': self._price,
        }


@app.get('/api/v1/d')
async def get_v1d(
    # * dependency one
    app_version: Annotated[int, Depends(get_app_version)],
    # * dependency two
    random_number: Annotated[int, Depends(any_random_number)],
    # * Dependency as Class
    car: Annotated[Car, Depends(Car)],
):
    return {
        'path': 'v1/d',
        'version': app_version,
        'user_count': random_number,
        # * you can call members or/and members as needed.
        'car': car.info(),
    }


@app.get('/api/v1/e')
async def get_v1e(
    # * dependency one
    app_version: Annotated[int, Depends(get_app_version)],
    # * dependency two
    random_number: Annotated[int, Depends(any_random_number)],
    # * Dependency as Class
    # ~ define depends only in annotated
    car: Annotated[Car, Depends()],
):
    return {
        'path': 'v1/e',
        'version': app_version,
        'user_count': random_number,
        # * you can call members or/and members as needed.
        'car': car.info(),
    }


# * Dependency Chaining (or) Sub Dependency


async def is_expired(
    scope_expiry: Annotated[datetime.date | None, Header()] = None,
) -> bool:
    if scope_expiry is None:
        return True
    print(
        scope_expiry,
        datetime.date.today(),
        scope_expiry > datetime.date.today(),
    )
    return scope_expiry < datetime.date.today()


async def get_scope(
    expired: Annotated[bool, Depends(dependency=is_expired)],
    scopes: Annotated[str | None, Header()] = None,
) -> dict[str, Iterable[str]]:
    print(scopes)
    if scopes is None or expired:
        return {'scopes': ()}
    return {'scopes': scopes.split(' ')}


@app.get('/api/v1/f')
async def get_v1f(
    user_scopes: Annotated[dict[str, Iterable[str]], Depends(get_scope)],
):
    return user_scopes


# * Dependency in Path Operation decorator


async def access_token(X_Access_Token: Annotated[str | None, Header()] = None):
    if X_Access_Token != 'fake-user-account-token':
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    # * is not used in path operation
    return {}


@app.get(
    '/api/v1/g',
    dependencies=[
        # * You can define any number of dependencies here.
        Depends(access_token),
    ],
)
async def get_v1g():
    return {'Message': 'Hello'}
