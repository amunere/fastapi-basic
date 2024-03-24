import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .routes import get_apps_router, TimedRoute


def get_application():
    _app = FastAPI(title=settings.APP_NAME)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
      
    return _app


app = get_application()


@app.get("/111")
async def root():
    return {"message": "main"}

app.include_router(get_apps_router()) #, prefix="/api/v1"

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)