from api_models import Token
from fastapi import FastAPI, HTTPException, Query, status
from pydantic import AfterValidator
from typing import Annotated

import re


app: FastAPI = FastAPI()


"""
parameters that are not included path parameters are "query parameter".
"""


@app.get('/books')
async def book_list(
    # * Optional Queries
    start: int = 0,
    end: int = 0,
):
    """
    Query with Default Values
    `start` and `end` will have default values if not given.
    """
    message = {
        'message': 'Query Parameter',
        'Query - Params': {
            'start': start,
            'end': end,
        },
    }
    return message


@app.get('/read')
async def read_book(
    # * Required Query
    book_id: int,
    # * Optional Queries
    author: str | None = None,
    exclude_old: bool = False,
):
    """
    `book_id`     - Query Parameter is Required. (Should be Integer.)
    `author`      - Query Parameter is Not Required
                    (Accepts String only if passed else None)
    `exclude_old` - A Boolean Value [on off 1 0 yes no true false]
                    Automatically converted to boolean
    """
    message = {
        'message': 'Query Parameter',
        'Query - Params': {'BookID': book_id},
    }
    if author:
        message['Query - Params']['Author'] = author
    if exclude_old:
        message['Query - Params']['BookCounrt'] = 'Less'
    else:
        message['Query - Params']['BookCount'] = 'More'
    return message


""" Advanced Query Options """


@app.get('/fruits')
def fruits(
    # * Query with default value [ Optional Queries ]
    query: Annotated[list[str] | None, Query()] = None,
):
    """query list"""
    if query is None:
        return {'message': 'fruits', 'query': 'Nothing Passed'}
    return {'message': 'Hello World', 'query': query}


@app.get('/update')
async def update_book_present(
    # * Optional Query
    book_id: Annotated[list[int] | None, Query()] = None,
):
    """query list"""
    'book_id - list of Query Params'
    message = {
        'message': 'Query Parameter',
        'Query - Params': {},
    }
    print(book_id)
    if book_id is not None:
        message['Query - Params']['BookIDs'] = book_id
        message['Query - Params']['detail'] = 'added'
    return message


@app.get('/text')
async def textQuery(
    # * Optional Query
    query: Annotated[
        str | None,
        Query(
            min_length=6,
            max_length=13,
            pattern=r'^[1-9]?[a-f]\d+$',
        ),
    ] = None,
) -> dict[str, str]:
    return {
        'info': 'Query Validation',
        'query': query if query else 'No Query Supplied',
    }


def credit_card_validator(card_number: str) -> str:
    striped: str = card_number.replace(' ', '')
    odd = [int(x) for i, x in enumerate(striped) if i % 2 == 0]
    even = [int(x) for i, x in enumerate(striped) if i % 2 == 1]
    _a = sum(odd) * 2
    _b = sum(even[:-1]) * 2
    # print(_b - _a)
    # print(odd, sum(odd) * 2)
    # print(even, sum(even[:-1]) * 2, even[:-1])
    if (_b - _a) == 0:
        return card_number
    else:
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail={'status': 'invalid credit card'},
        )


@app.get('/card/validate')
async def validate_credit_card(
    # * Required Query
    card_number: Annotated[
        str,
        # * Performs Fastapi validation then Perform Custom Validation logic
        Query(
            title='Validate Credit Card',
            description='validate credit card number',
            min_length=19,
            max_length=19,
            # * regex pattern to match
            pattern=r'^[3-9][0-9]{3}\ [0-9]{4}\ [0-9]{4}\ [0-9]{4}$',
            # * Alternate name for the query `card_number`
            # *    client must send `{"credit card": "3458 2389 2938 4283"}` as query
            alias='credit card',
        ),
        AfterValidator(credit_card_validator),
    ],
) -> dict[str, dict[str, str] | str]:
    print(card_number)
    return {
        'message': 'Query With Validation Function.',
        'detail': {'Credit Card Number': card_number},
    }


""" Query as Pydantic model """


def validate_token(token: Token):
    print(token, len(token.token))
    if token.encrypted and re.match(
        r'^[5-9a-lM-Z]{16}$', token.token.split(' ')[-1]
    ):
        return token
    elif re.match(r'^[0-4m-zA-L]{24}$', token.token.split(' ')[-1]):
        return token
    raise HTTPException(
        status.HTTP_403_FORBIDDEN, detail={'message': 'invalid bearer token.'}
    )


@app.get('/token')
async def perform_some_operations(
    token: Annotated[Token, Query(), AfterValidator(validate_token)],
):
    return token
