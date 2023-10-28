from fastapi import APIRouter

from src.api.os import handle_os

router = APIRouter()

router.include_router(handle_os.router, prefix="/handle")
