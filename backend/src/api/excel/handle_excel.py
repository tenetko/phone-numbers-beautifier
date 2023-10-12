from fastapi import APIRouter, Response, UploadFile

from src.core.excel_handler.excel_handler import ExcelHandler

router = APIRouter()


@router.post("/")
async def handle_xlsx_files(files: list[UploadFile]) -> Response:
    handler = ExcelHandler(files, "tzb")
    response = handler.run()

    return response
