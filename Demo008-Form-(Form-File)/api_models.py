from pydantic import BaseModel, EmailStr, Field, SecretStr


class Login(BaseModel):
    # ! Forbid users sending extra form field to server
    model_config = {'extra': 'forbid'}
    #
    email: EmailStr
    password: SecretStr = Field(exclude=True)
