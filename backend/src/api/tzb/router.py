from fastapi import APIRouter

from src.api.tzb import handle_tzb

router = APIRouter()

router.include_router(handle_tzb.router, prefix="/handle")
