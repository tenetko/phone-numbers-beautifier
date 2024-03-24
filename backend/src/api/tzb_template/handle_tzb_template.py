from typing import Annotated

from fastapi import APIRouter, Form, Response, UploadFile

from src.core.tzb_template_handler.tzb_template_handler import TZBTemplateHandler

router = APIRouter()


@router.post("/")
async def handle_tzb_files(files: list[UploadFile]) -> Response:
    handler = TZBTemplateHandler(files)
    response = handler.run()

    return response
