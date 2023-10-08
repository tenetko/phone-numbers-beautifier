from fastapi import APIRouter, File, UploadFile
from typing import Annotated

router = APIRouter()

@router.post("/")
async def handle_xlsx_files(files: list[UploadFile]):
    print([file.filename for file in files])
