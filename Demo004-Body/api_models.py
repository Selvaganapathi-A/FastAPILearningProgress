from dateutil.relativedelta import relativedelta
from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Any

import datetime


class User(BaseModel):
    firstname: str
    lastname: str | None = None
    email: EmailStr
    dateofbirth: datetime.date
    state: str | None = None
    province: str | None = None
    country: str | None = None

    @model_validator(mode='before')
    @classmethod
    def check_age(
        cls: type['User'], initial_data: dict[Any, Any]
    ) -> dict[Any, Any]:
        print(initial_data)
        if (
            relativedelta(
                datetime.date.today(),
                datetime.date.fromisoformat(initial_data['dateofbirth']),
            ).years
            < 18
        ):
            raise ValueError('Continue After 18 Years old.')
        return initial_data


class Product(BaseModel):
    product_id: int | None = None
    category: str
    name: str
    price: float
    taxable: bool = False


class ProductPatch(BaseModel):
    product_id: int | None = None
    category: str | None = None
    name: str | None = None
    price: float | None = None
    taxable: bool | None = None


class Student(BaseModel):
    rollno: int
    name: str
    std: str


class Province(BaseModel):
    name: str
    declared: int


class State(BaseModel):
    name: str
    declared: int
    # nested model
    province: list[Province] | None = None
    #
    tags: set[str] = Field(default_factory=set)
