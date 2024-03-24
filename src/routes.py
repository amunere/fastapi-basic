from datetime import time
from typing import Callable
from fastapi import APIRouter, Request, Response
from src.user import router as user_router
from src.auth import router as auth_router
from fastapi.routing import APIRoute



class TimedRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            before = time.time()
            response: Response = await original_route_handler(request)
            duration = time.time() - before
            response.headers["X-Response-Time"] = str(duration)
            print(f"route duration: {duration}")
            print(f"route response: {response}")
            print(f"route response headers: {response.headers}")
            return response

        return custom_route_handler
    

def get_apps_router():
    api_router = APIRouter(route_class=TimedRoute)
    api_router.include_router(auth_router.router, prefix="/auth", tags=["auth"])
    api_router.include_router(user_router.router, prefix="/users", tags=["users"])
    return api_router