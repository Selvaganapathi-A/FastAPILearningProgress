from fastapi import APIRouter, Depends, security
from pprint import pprint
from typing import Annotated

from .auth import create_token
from .password import hash_password


router = APIRouter()


@router.post('/token')
async def login_for_access_token(
    form: Annotated[security.OAuth2PasswordRequestForm, Depends()],
):
    # * Create Access Token
    form_data = {
        'client_id': form.client_id,
        'client_secret': form.client_secret,
        'grant_type': form.grant_type,
        'scopes': form.scopes,
        'password': form.password,
        'password_hash': await hash_password(form.password),
        'username': form.username,
    }
    pprint(form_data)
    #
    return {
        'token': await create_token(
            {
                'username': form.username,
                # 'scopes': ['manager', 'admin', 'cto', 'cfo'],
            },
        )
    }
