from pydantic import BaseModel


class EvChargersResponse(BaseModel):
    chargerCount: int
    stationCount: int
    stations: list[dict]
