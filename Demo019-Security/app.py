from fastapi import Depends, FastAPI, security, Security
from flow_3_OAuth2PasswordBearer_SecurityScopes.auth import get_username
from typing import Annotated

import flow_1_apiKey.app
import flow_2_OAuth2AuthorizationBearer.app
import flow_3_OAuth2PasswordBearer_SecurityScopes.main
import flow_4_HttpBasic.app
import flow_5_HttpDigest.app
import flow_6_HttpBearer.app


app: FastAPI = FastAPI()


app.include_router(
    flow_1_apiKey.app.router,
    prefix='/api/demo/apiKey',
)


app.include_router(
    flow_2_OAuth2AuthorizationBearer.app.router,
    prefix='/api/demo/OAuth2Bearer',
)


app.include_router(
    flow_3_OAuth2PasswordBearer_SecurityScopes.main.router,
    prefix='/api/demo/OAuth2',
)


app.include_router(
    flow_4_HttpBasic.app.router,
    prefix='/api/demo/HttpBasic',
)


app.include_router(
    flow_5_HttpDigest.app.router,
    prefix='/api/demo/HttpDigest',
)


app.include_router(
    flow_6_HttpBearer.app.router,
    prefix='/api/demo/HttpBearer',
)


# app.include_router(flow_1_apiKey.app.router, prefix='/api/key')
# app.include_router(
#     flow_2_OAuthPassword.app.router, prefix='/api/oAuth/password'
# )
# app.include_router(
#     flow_3_OAuth2AuthorizationBearer.app.router, prefix='/api/oAuth/AuthBearer'
# )


# ~ ================================================= ~ #


@app.get('/birds')
async def get_birds(
    user: Annotated[
        str,
        Security(
            get_username,
            # * need atleast manager permissions
            scopes=['admin', 'manager'],
        ),
    ],
):
    return {'route': '/birds', 'message': user}
