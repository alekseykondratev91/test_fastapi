from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT

from app.database.models.user import User
from app.schemas.secret_schemas import SecretResponse
from app.schemas.user_schemas import UserLogin, UserResponse
from app.utils.user_utils import get_salt, hash_password, validate_password

router = APIRouter()


@router.post(
    "/user.create_account",
    response_description="Create new user account",
    response_model=UserResponse,
)
async def create_account(user: User, authorize: AuthJWT = Depends()) -> UserResponse:
    user_db = await User.find_one({"email": user.email})
    if user_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    salt = get_salt()
    hashed_password = hash_password(
        password=user.password,
        salt=salt,
    )
    user.password = f"{salt}${hashed_password}"
    await user.create()
    access_token = authorize.create_access_token(subject=user.email)
    refresh_token = authorize.create_refresh_token(subject=user.email)
    authorize.set_access_cookies(access_token)
    authorize.set_refresh_cookies(refresh_token)
    return UserResponse(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
    )


@router.post(
    "/user.login", response_description="Login user", response_model=UserResponse
)
async def login_user(user: UserLogin, authorize: AuthJWT = Depends()):
    user_db = await User.find_one({"email": user.email})
    if not user_db:
        raise HTTPException(status_code=400, detail="Incorrect email")
    if not validate_password(
        password=user.password,
        hashed_password=user_db.password,
    ):
        raise HTTPException(status_code=401, detail="Invalid password")
    access_token = authorize.create_access_token(subject=user.email)
    refresh_token = authorize.create_refresh_token(subject=user.email)
    authorize.set_access_cookies(access_token)
    authorize.set_refresh_cookies(refresh_token)
    return UserResponse(
        first_name=user_db.first_name,
        last_name=user_db.last_name,
        email=user_db.email,
    )


@router.get("/user.list_secrets", response_model=UserResponse)
async def list_my_secrets(authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    current_user = await User.find_one({"email": authorize.get_jwt_subject()})
    await current_user.fetch_all_links()
    return UserResponse(
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        email=current_user.email,
        secrets=[
            SecretResponse(secret_key=secret.id, secret_name=secret.secret_name)
            for secret in current_user.secrets
        ],
    )


@router.delete("/user.logout")
async def logout(authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    authorize.unset_jwt_cookies()
    return {"msg": "Successfully logout"}
