from fastapi import APIRouter

router = APIRouter(
    prefix="/api",
    tags=["events_provider"],
)
