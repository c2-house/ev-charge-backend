from fastapi_mctools.dependencies import Dependency
from app.services.chargers import get_organized_chargers


dependencies = Dependency(Chargers=get_organized_chargers)
