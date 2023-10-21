from fastapi import APIRouter
from app.routes.apis import router as api_router

router = APIRouter()

router.include_router(api_router, prefix="/api")
