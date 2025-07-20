from fastapi import FastAPI
from routes import auth, crud


app: FastAPI = FastAPI()


app.include_router(
    auth.router,
    prefix='/auth',
    tags=[
        'authendication',
    ],
)

app.include_router(
    crud.router,
    prefix='/items',
    tags=['items', 'product'],
)
