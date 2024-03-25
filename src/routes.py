from datetime import time
from typing import Callable
from fastapi import APIRouter, Request, Response
from src.user import router as user_router
from src.auth import router as auth_router
from fastapi.routing import APIRoute


def get_apps_router():
    api_router = APIRouter()
    api_router.include_router(auth_router.router, prefix="/auth", tags=["auth"])
    api_router.include_router(user_router.router, prefix="/users", tags=["users"])
    return api_router