from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_mctools.utils.requests import APIClient


states = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        api_client = APIClient()
        await api_client.start()
        states["api_client"] = api_client
        yield
    finally:
        await api_client.close()
        del states["api_client"]
