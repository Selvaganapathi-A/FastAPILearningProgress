from api_models import CookieModel
from fastapi import Cookie, FastAPI, Request, Response
from fastapi.middleware import cors
from typing import Annotated


app: FastAPI = FastAPI()


@app.get('/api/v/1/a')
async def v1a(
    # * read Cookies
    previous_visits: Annotated[
        int | None,
        Cookie(
            title='Track Previous Visits',
            description=(
                'If visits Previously Hide Banners '
                'that are intended for new users'
            ),
        ),
    ] = None,
) -> dict[str, int]:
    return {
        'Previous Visit Count To This Site': 0
        if previous_visits is None
        else previous_visits
    }


@app.get('/api/v/1/b')
async def v1b(
    response: Response,
    previous_visits: Annotated[
        int | None,
        Cookie(
            title='Track Previous Visits',
            description='If visits Previously Hide Banners that are intended for new users',
        ),
    ] = None,
) -> dict[str, str | int]:
    # * Read and write Cookies
    pv: int = 0
    if previous_visits is None:
        pv = 1
    else:
        pv = previous_visits + 1
    # ! this also set set cookie header
    response.set_cookie(
        'previous_visits',
        f'{pv}',
        max_age=18000,
        httponly=True,
    )
    return {'message': 'Hello', 'previous_visits': pv + 1}


""" Advanced """


@app.get('/api/v/1/c')
async def cookie_model(model: Annotated[CookieModel, Cookie()]):
    return model
