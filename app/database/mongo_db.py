import motor.motor_asyncio
from beanie import init_beanie

from app.web.settings import settings


async def init_mongo_db() -> None:
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongo_url)
    await init_beanie(database=client.db_name)
