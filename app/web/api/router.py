from fastapi import APIRouter

from app.web.api import monitoring, secrets, user

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(user.router)
api_router.include_router(secrets.router)
