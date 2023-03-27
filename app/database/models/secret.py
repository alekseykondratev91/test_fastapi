from typing import Union

from beanie import Document
from pydantic import Field


class Secret(Document):
    secret_name: str = Field(...)
    code_phrase: str = Field(...)
    secret_body: Union[str, bytes] = Field(...)

    class Settings:
        name = "secrets"

    class Config:
        schema_extra = {
            "example": {
                "secret_name": "MySecret",
                "code_phrase": "My code phrase",
                "secret_body": "Lorem ipsum dolor sit amet, consectetur adipiscing elit",
            }
        }
