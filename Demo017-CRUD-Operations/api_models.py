from pydantic import BaseModel


class HeroBase(BaseModel):
    name: str
    age: int | None = None


class Hero(HeroBase):
    pk: int | None = None
    secret_name: str


class HeroPublic(HeroBase):
    pk: int


class HeroCreate(HeroBase):
    secret_name: str


class HeroUpdate(BaseModel):
    name: str | None = None
    secret_name: str | None = None
    age: int | None = None
