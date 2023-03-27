from beanie import PydanticObjectId, WriteRules
from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT

from app.database.models.secret import Secret
from app.database.models.user import User
from app.schemas.secret_schemas import SecretRequest
from app.utils.secret_utils import decrypt_secret, encrypt_secret
from app.utils.user_utils import get_salt, hash_password, validate_password

router = APIRouter()


@router.post("/generate_secret", response_description="Generate new secret")
async def generate_secret(secret: Secret, authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    current_user = await User.find_one({"email": authorize.get_jwt_subject()})
    if not current_user:
        raise HTTPException(status_code=403, detail="Forbidden")
    secret.secret_body = encrypt_secret(secret)
    salt = get_salt()
    code_phrase = hash_password(
        password=secret.code_phrase,
        salt=salt,
    )
    secret.code_phrase = f"{salt}${code_phrase}"
    if not current_user.secrets:
        current_user.secrets = [secret]
    current_user.secrets.append(secret)
    await current_user.save(link_rule=WriteRules.WRITE)
    return {"msg": "Secret generate successfully", "secret_key": secret.id}


@router.get("/secrets/{secret_key}", response_description="Get secret by secret key")
async def get_secret_by_secret_key(
    secret_key: PydanticObjectId, search_secret: SecretRequest
):
    secret = await Secret.get(secret_key)
    if not validate_password(
        password=search_secret.code_phrase,
        hashed_password=secret.code_phrase,
    ):
        raise HTTPException(status_code=401, detail="Invalid secret code phrase")
    secret_data = decrypt_secret(secret, search_secret.code_phrase)
    return {"secret": secret_data}
