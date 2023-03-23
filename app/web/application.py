from fastapi import FastAPI
from fastapi.responses import UJSONResponse

from app.web.api.router import api_router
from app.web.lifetime import register_startup_events


def get_app() -> FastAPI:
    app = FastAPI(
        title="Secret App",
        default_response_class=UJSONResponse,
    )
    register_startup_events(app)

    app.include_router(router=api_router, prefix="/api")

    return app
