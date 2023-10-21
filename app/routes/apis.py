from fastapi import APIRouter, status
from app.schemas.chargers import EvChargersResponse
from app.services.chargers import Chargers


router = APIRouter()


@router.get(
    "/chargers", status_code=status.HTTP_200_OK, response_model=EvChargersResponse
)
async def get_chargers(results: Chargers):
    return results
