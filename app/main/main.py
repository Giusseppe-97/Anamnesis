from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from api.api import api_router
from core.config import settings
from utils.storage_utils import review_local_dirs

review_local_dirs()

app = FastAPI(
    title=settings.PROJECT_NAME
)

if settings.CORS_ALLOW_CUSTOM_ORIGINS_FLAG:
    allow_origins = settings.DEVELOPMENT_CORS_ORIGINS
    if settings.PRODUCTION:
        allow_origins = settings.PRODUCTION_CORS_ORIGINS

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

@app.get("/")
def read_root():
    return {"Hello": "este es el el ambiente de desarollo en prouducción para hacer pruebas:"}

app.include_router(api_router, prefix=settings.API_STR)
