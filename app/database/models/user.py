from typing import List, Optional

from beanie import Document, Indexed, Link
from pydantic import Field
from pydantic.networks import EmailStr

from app.database.models.secret import Secret


class User(Document):
    first_name: str = Field(...)
    last_name: str = Field(...)
    password: str = Field(...)
    email: Indexed(EmailStr, unique=True)
    secrets: Optional[List[Link[Secret]]] = None

    class Settings:
        name = "user"

    class Config:
        schema_extra = {
            "example": {
                "first_name": "Monty",
                "last_name": "Python",
                "password": "password",
                "email": "username@email.com",
            }
        }
