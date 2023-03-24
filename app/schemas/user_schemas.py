from pydantic import BaseModel, EmailStr, Field


class UserLogin(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {"password": "password", "email": "username@email.com"}
        }


class UserResponse(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

    class Config:
        schema_extra = {
            "example": {
                "first_name": "Monty",
                "last_name": "Python",
                "email": "username@email.com",
            }
        }