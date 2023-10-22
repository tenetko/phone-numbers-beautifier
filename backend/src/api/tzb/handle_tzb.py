from fastapi import APIRouter, Response, UploadFile

from src.core.tzb_handler.tzb_handler import TZBHandler

router = APIRouter()


@router.post("/")
async def handle_tzb_files(files: list[UploadFile]) -> Response:
    handler = TZBHandler(files, "tzb")
    response = handler.run()

    return response
