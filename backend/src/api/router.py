from fastapi import APIRouter

from src.api.reminders.router import router as reminders_router
from src.api.root.router import router as root_router
from src.api.tzb.router import router as tzb_router

api_router = APIRouter()
static_router = APIRouter()

api_router.include_router(tzb_router, prefix="/tzb")
api_router.include_router(reminders_router, prefix="/reminders")
static_router.include_router(root_router)
