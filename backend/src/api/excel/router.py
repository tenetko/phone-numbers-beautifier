from fastapi import APIRouter

from src.api.excel import handle_excel

router = APIRouter()

router.include_router(handle_excel.router, prefix="/handle")
