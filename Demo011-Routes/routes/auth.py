from fastapi import APIRouter, Form, Header
from typing import Annotated

import random


router: APIRouter = APIRouter()


@router.post('/login')
async def login(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
):
    return {
        'message': 'login_with_token',
        'credentials': {
            'username': username,
            'password': password,
        },
    }


@router.post('/v2/login')
async def login_v2(token: Annotated[str, Header()]):
    return {
        'message': 'login_with_token',
        'token': token,
    }


@router.post('/signup')
async def signup(
    firstname: Annotated[str, Form()],
    email: Annotated[str, Form()],
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    lastname: Annotated[str | None, Form()] = None,
):
    return {
        'message': 'create new user',
        'userinfo': {
            'id': random.randint(1, 1000),
            'firstname': firstname,
            'lastname': lastname,
            'email': email,
            'username': username,
            # ~ 'password': password,
        },
    }
