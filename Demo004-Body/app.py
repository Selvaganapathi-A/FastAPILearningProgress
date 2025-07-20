from api_models import Product, ProductPatch, Province, State, Student, User
from fastapi import Body, FastAPI, HTTPException, Path, Query, status
from fastapi.encoders import jsonable_encoder
from typing import Annotated

import asyncio


app: FastAPI = FastAPI()


@app.post('/user')
async def upload_user(user: User):
    """Body as JSON Format"""
    return {'message': 'Body Parameter', 'content': user}


@app.put('/user/{user_id}')
async def update_user(user_id: int, user: User, fake: bool = False):
    """
    user_id : int        - path_parameter
    user    : User Model - request body {Body}
    fake    : bool       - { Query }
    """
    print(fake)
    if fake:
        return {
            'message': 'Body & Path Parameter',
            'detail': {
                'user': user,
                'action': 'faking Process',
                'ID': user_id,
            },
        }
    else:
        await asyncio.sleep(2)
        return {
            'message': 'Body & Path Parameter',
            'detail': {
                'user': user,
                'action': 'update user details in database',
                'ID': user_id,
            },
        }


""" Single, embedded and Nested Body Content """

"""
in `post`, `put`, `patch` http-methods
pydantic models are considered `body`,
whereas single elements considered `query` if not specified as `path` or `body`


note :-
    path, query, body params can be in any order.
"""


@app.put('/items/{item_id}')
async def multiple_args(
    *,
    # * Path parameter
    item_id: int,
    # * it can be as follows too
    # item_id: Annotated[int, Path()],
    #
    # * Query
    rate_conversion: str,
    # * it can be as follows too
    # rate_conversion: Annotated[str, Query()],
    #
    # * Body as Pydantic Model
    product: Product,
    #
    # * Single Body Content
    rating: Annotated[int, Body(ge=0, lt=5)],
    #
):
    return {
        'path param': {'item_id': item_id},
        'body': {
            'complex body': {'product': product},
            'inline body': {
                'rating': rating,
            },
        },
        'query': rate_conversion,
    }


@app.put('/api/v1/student/')
async def student_v1(
    # * Body Embed
    student: Annotated[Student, Body(embed=True)],
):
    return {
        'type': 'embed',
        'student': student,
    }


@app.put('/api/v2/student/')
async def student_v2(
    # * Body not Embed
    student: Annotated[Student, Body(embed=False)],
):
    return {
        'type': 'not embed',
        'student': student,
    }


"""
complex body models
 - nested models
 - list, set datatypes [used in 'checkbox' options]
 - model field options
"""


@app.put('/api/v1/state')
async def manage_state(
    state: Annotated[
        State,
        Body(
            examples=[
                {
                    'name': 'minnosotta',
                    'declared': 1920,
                },
                {
                    'name': 'seattle',
                    'declared': 19190,
                    'province': [
                        {
                            'name': 'arizona',
                            'declared': 1890,
                        },
                        {
                            'name': 'miami',
                            'declared': 1890,
                        },
                    ],
                },
                {
                    'name': 'seattle',
                    'declared': 19190,
                    'province': [
                        'north town',
                    ],
                    'tags': [
                        'work',
                        'tour',
                        'military',
                    ],
                },
            ],
            openapi_examples={
                'normal': {
                    'summary': 'A Short Description',
                    'description': 'Detailed Note may/maynot contain markdown text',
                    'value': {
                        # * Actual Value shown as example in docs,
                        'name': 'seattle',
                        'declared': 19190,
                        'province': [
                            'north town',
                        ],
                        'tags': [
                            'work',
                            'tour',
                            'military',
                        ],
                    },
                },
                'converted': {
                    'summary': 'A Short Description',
                    'description': '**Markdown** Text __as__ description.',
                    'value': {
                        # * Actual Value shown as example in docs,
                        'name': 'seattle',
                        'declared': 19190,
                        'province': [
                            'north town',
                        ],
                        'tags': [
                            'work',
                            'tour',
                            'military',
                        ],
                    },
                },
                'invalid': {
                    'summary': 'Invalid data that is rejected by API',
                    'description': 'View Below Example',
                    'value': {
                        # * Actual Value shown as example in docs,
                        'name': 12311,  # ! as int instead of string
                        'declared': 19190,
                        'province': [
                            'north town',
                        ],
                        'tags': 'work',  # ! singel tag instead of tag list
                    },
                },
                # 'invalid': {
                #     'summary': '',
                #     'description': '',
                #     'externalValue': {"url":'http://localhost:443/openapi/examples?openapi=v1'},
                # },
            },
        ),
    ],
):
    return {'state': state}


"""

Update a Model
use Patch to update model

"""

products: dict[str, Product] = {}


@app.post('/api/v1/product', status_code=status.HTTP_201_CREATED)
async def create_Product(product: Product):
    if product.name in products:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    products[product.name] = product
    return product


@app.get('/api/v1/product')
async def read_all_Product() -> dict[str, Product]:
    return products


@app.get('/api/v1/product/{product_id}')
async def read_Product(product_id: str) -> Product:
    if product_id not in products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return products[product_id]


@app.put('/api/v1/product/{product_id}')
async def replace_Product(product_id: str, product: Product) -> Product:
    if product_id not in products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    products[product_id] = product
    return product


@app.patch('/api/v1/product/{product_id}')
async def modify_Product(product_id: str, product: ProductPatch) -> Product:
    # * Updating data
    if product_id not in products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    client_product = product.model_dump(exclude_unset=True, exclude_none=True)
    server_product = products[product_id]
    #
    server_product_copy = server_product.model_copy(update=client_product)
    products[product_id] = server_product_copy
    #
    return server_product_copy


@app.delete('/api/v1/product/{product_id}')
async def delete_Product(product_id: str) -> dict[str, str]:
    if product_id not in products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    del products[product_id]
    return {'message': 'deleted'}
