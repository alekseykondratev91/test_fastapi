import motor.motor_asyncio
from beanie import init_beanie

from app.database.models.user import User
from app.web.settings import settings


async def init_mongo_db() -> None:
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongo_url)
    await init_beanie(database=client["secret_app"], document_models=[User])
