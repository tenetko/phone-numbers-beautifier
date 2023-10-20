from fastapi import APIRouter, Response, UploadFile

from src.core.reminders_handler.reminders_handler import RemindersHandler

router = APIRouter()


@router.post("/")
async def handle_reminders_files(files: list[UploadFile]) -> Response:
    handler = RemindersHandler(files)
    response = handler.run()

    return response
