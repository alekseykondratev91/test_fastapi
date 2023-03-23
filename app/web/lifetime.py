from typing import Awaitable, Callable

from fastapi import FastAPI

from app.database.mongo_db import init_mongo_db


def register_startup_events(app: FastAPI) -> Callable[[], Awaitable[None]]:
    @app.on_event("startup")
    async def _startup() -> None:
        await init_mongo_db()
        pass

    return _startup
