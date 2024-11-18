import uvicorn
from fastapi import FastAPI

from config import settings
from presentations.routes.sales import router as llm_router

app = FastAPI()

app.include_router(
    llm_router,
    prefix="/llm",
    tags=["llm"],
)
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.api_config.HOST,
        port=settings.api_config.PORT,
        reload=settings.api_config.RELOAD,
        workers=settings.api_config.WORKERS,
    )
