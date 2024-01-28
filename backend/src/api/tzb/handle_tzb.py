from fastapi import APIRouter, Form, Response, UploadFile
from typing import Annotated


from src.core.tzb_handler.tzb_handler import TZBHandler

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

    handler = TZBHandler(dates, files)
    response = handler.run()

    return response
