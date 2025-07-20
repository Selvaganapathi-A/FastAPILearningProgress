from pydantic import BaseModel


class CookieModel(BaseModel):
    language: str | None = None
    ad_id: str
    click_id: int
