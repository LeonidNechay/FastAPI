from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from session import Base
from pydantic import BaseModel


class Author(BaseModel):
    id: int
    name: str

class AuthorList(BaseModel):
    data: List[Author]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "data": [
                        {
                          "id": 1,
                          "name": "author1"
                        },
                        {
                            "id": 2,
                            "name": "author2"
                        },
                        {
                          "id": 3,
                          "name": "author3"
                        },
                      ]
                }
            ]
        }
    }

class Book(BaseModel):
    id: int
    name: str

    author_name: str


class Authors(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))

class Books(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))

    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))



class Brand(BaseModel):
    id: int
    name: str

class Vehicles(BaseModel):
    id: int
    name: str
    year: int
    type: str

    brand: Brand


class Motobike(Vehicles):
    type: str = 'Motobike'
