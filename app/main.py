from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.routers import router as api_router


app = FastAPI()

app.include_router(api_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ev-charge.kr", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
