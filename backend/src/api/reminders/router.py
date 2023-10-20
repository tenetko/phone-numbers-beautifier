from fastapi import APIRouter

from src.api.reminders import handle_reminders

router = APIRouter()

router.include_router(handle_reminders.router, prefix="/handle")
