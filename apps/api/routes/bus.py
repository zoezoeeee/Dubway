from fastapi import APIRouter

from services.gtfs import get_live_bus_response

router = APIRouter()


@router.get("/live/bus")
def live_bus(query: str):
    """
    User-facing bus endpoint.

    The frontend has a single text input. The user may enter either:
    - a stop number, such as 842
    - a stop name, such as Abbey Street

    We resolve that value to the GTFS stop_id before querying the realtime API.
    """
    return get_live_bus_response(query)
