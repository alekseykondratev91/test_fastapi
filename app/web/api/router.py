from fastapi import APIRouter

from app.web.api import monitoring

api_router = APIRouter()
api_router.include_router(monitoring.router)
