from beanie import Document, Indexed
from pydantic import Field
from pydantic.networks import EmailStr


class User(Document):
    first_name: str = Field(...)
    last_name: str = Field(...)
    password: str = Field(...)
    email: Indexed(EmailStr, unique=True)

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
