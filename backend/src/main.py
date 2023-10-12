from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.api.router import api_router, static_router

app = FastAPI(title="Phone Numbers Beautifier Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(static_router)
app.include_router(api_router, prefix="/api")
app.mount("/", StaticFiles(directory="static"), "static")
