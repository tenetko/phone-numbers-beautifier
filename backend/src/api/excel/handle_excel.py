from fastapi import APIRouter, File, UploadFile
from typing import Annotated

router = APIRouter()

@router.post("/")
async def handle_xlsx_files(file: UploadFile):
    return file.filename