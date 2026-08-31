from fastapi import APIRouter

from services.gtfs import search_station_code

router = APIRouter()


@router.get("/stations/search")
def search_stations(q: str):
    return search_station_code(q)
