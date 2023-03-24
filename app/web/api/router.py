from fastapi import APIRouter

from app.web.api import monitoring, user

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(user.router)
