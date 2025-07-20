from pydantic import BaseModel, EmailStr, SecretStr

import datetime


class UserIn(BaseModel):
    first_name: str
    last_name: str | None = None
    date_of_birth: datetime.date | None
    email: EmailStr
    password: SecretStr


class UserOut(BaseModel):
    first_name: str
    last_name: str | None = None
    date_of_birth: datetime.date | None
    email: EmailStr
