from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException

from app.utils.auth_utils import authjwt_exception_handler
from app.web.api.router import api_router
from app.web.lifetime import register_startup_events


def get_app() -> FastAPI:
    app = FastAPI(
        title="Secret App",
        default_response_class=UJSONResponse,
    )
    register_startup_events(app)

    app.include_router(router=api_router, prefix="/api")

    app.add_exception_handler(
        exc_class_or_status_code=AuthJWTException, handler=authjwt_exception_handler
    )

    return app
