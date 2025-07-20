from pydantic import BaseModel


class Token(BaseModel):
    # query params
    token: str
    encrypted: bool = False
    # forbid sending extra queries with the request
    model_config = {'extra': 'forbid'}
