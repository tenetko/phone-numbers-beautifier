from fastapi import APIRouter

from src.api.tzb_template import handle_tzb_template

router = APIRouter()

router.include_router(handle_tzb_template.router, prefix="/handle")
