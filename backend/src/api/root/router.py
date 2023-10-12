from fastapi import APIRouter

from src.api.root import root

router = APIRouter()

router.include_router(root.router)
