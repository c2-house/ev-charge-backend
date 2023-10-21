from fastapi import FastAPI
from app.routes.routers import router as api_router


app = FastAPI()

app.include_router(api_router)
