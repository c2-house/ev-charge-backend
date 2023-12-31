from fastapi import Depends, APIRouter, status
from app.schemas.chargers import EvChargersResponse
from app.services.requests import check_secret_header
from app.services.dependencies import dependencies

router = APIRouter()


@router.get(
    "/chargers",
    dependencies=[Depends(check_secret_header)],
    status_code=status.HTTP_200_OK,
    response_model=EvChargersResponse,
)
async def get_chargers(results: dependencies.Chargers):
    return results
