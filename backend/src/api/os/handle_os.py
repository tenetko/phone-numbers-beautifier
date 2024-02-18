from fastapi import APIRouter, Response, UploadFile

from src.core.os_handler.os_handler import OSHandler

router = APIRouter()


@router.post("/")
async def handle_os_files(files: list[UploadFile]) -> Response:
    handler = OSHandler(files)
    response = handler.run()

    return response
