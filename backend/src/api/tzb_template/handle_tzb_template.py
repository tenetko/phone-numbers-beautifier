from typing import Annotated

from fastapi import APIRouter, Form, Response, UploadFile

from src.core.tzb_template_handler.tzb_template_handler import TZBTemplateHandler

router = APIRouter()


@router.post("/")
async def handle_tzb_files(
    source_1_date_0: Annotated[str, Form()],
    source_1_date_1: Annotated[str, Form()],
    source_2_date_0: Annotated[str, Form()],
    source_2_date_1: Annotated[str, Form()],
    files: list[UploadFile],
) -> Response:
    dates = {
        "source_1_date_0": source_1_date_0,
        "source_1_date_1": source_1_date_1,
        "source_2_date_0": source_2_date_0,
        "source_2_date_1": source_2_date_1,
    }

    handler = TZBTemplateHandler(dates, files)
    response = handler.run()

    return response
