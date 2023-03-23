import uvicorn

from app.web.settings import settings


def main() -> None:
    uvicorn.run(
        "app.web.application:get_app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        factory=True,
    )


if __name__ == "__main__":
    main()
