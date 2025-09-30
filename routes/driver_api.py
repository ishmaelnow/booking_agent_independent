from fastapi import APIRouter
from db.driver_registry import list_available_drivers

router = APIRouter(prefix="/drivers", tags=["Drivers"])

@router.get("/available")
def get_available_drivers():
    drivers = list_available_drivers()
    return {"available_drivers": drivers}