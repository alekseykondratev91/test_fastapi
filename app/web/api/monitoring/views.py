from fastapi import APIRouter

router = APIRouter()


@router.get("/heals")
async def heals_check() -> None:
    ...
