from beanie import Document
from pydantic import Field
from pydantic.networks import EmailStr


class User(Document):
    username: str = Field(...)
    password: str = Field(...)
    email: EmailStr = Field(...)

    class Settings:
        name = "user"

    class Config:
        schema_extra = {
            "example": {
                "username": "Username",
                "password": "SHA256-password",
                "email": "username@email.com"
            }
        }