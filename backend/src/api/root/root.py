from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()


@router.get("/")
def get_root_page():
    return FileResponse("./static/index.html", status_code=200)
