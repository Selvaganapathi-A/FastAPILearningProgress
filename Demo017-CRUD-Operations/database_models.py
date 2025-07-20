from database import BASE
from sqlalchemy import engine, Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class Hero(BASE):
    __tablename__: str = 'Hero'
    pk: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    secret_name: Mapped[str] = mapped_column(String)
    age: Mapped[int] = mapped_column(Integer, nullable=True)

    def __repr__(self):
        return f'Hero( {self.name} )'
