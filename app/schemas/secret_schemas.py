from beanie import PydanticObjectId
from pydantic import BaseModel


class SecretResponse(BaseModel):
    secret_key: PydanticObjectId
    secret_name: str


class SecretRequest(BaseModel):
    code_phrase: str
