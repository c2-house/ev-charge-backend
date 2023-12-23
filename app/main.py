import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi_mctools.middlewares.logging import RequestLoggingMiddleware
from app.routes.routers import router as api_router
from app.core.config import app_settings


app = FastAPI()
logger = logging.getLogger("request")

app.include_router(api_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ev-charge.kr", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=app_settings.ALLOWED_HOSTS)
app.add_middleware(
    RequestLoggingMiddleware,
    logger=logger,
)
