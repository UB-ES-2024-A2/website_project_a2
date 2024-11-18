""" Main application module """
import sentry_sdk
from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware

from app.api.main import api_router
from app.core.config import settings


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"

if settings.SENTRY_DSN:
    sentry_sdk.init(dsn=str(settings.SENTRY_DSN), enable_tracing=True)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://polite-plant-051af6c03.5.azurestaticapps.net/"],
    allow_credentials=True,
    allow_methods=[""],  # Permite todos los métodos HTTP (GET, POST, etc.)
    allow_headers=[""],  # Permite todos los encabezados
)

app.include_router(api_router, prefix=settings.API_V1_STR)
