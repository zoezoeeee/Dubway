from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from services.gtfs import (
    get_live_bus_response,
    get_live_train_response,
    resolve_stop_id,
    search_station_code,
)


app = FastAPI()

bus_cache: dict[str, tuple[list[dict], float]] = {}
CACHE_TTL_SECONDS = 20

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/stations/search")
def search_stations(q: str):
    return search_station_code(q)


@app.get("/live/bus")
def live_bus(query: str):
    """
    User-facing bus endpoint.

    The frontend has a single text input. The user may enter either:
    - a stop number, such as 842
    - a stop name, such as Abbey Street

    We resolve that value to the GTFS stop_id before querying the realtime API.
    """
    return get_live_bus_response(query)


@app.get("/live/train")
def live_train(station_code: str):
    return get_live_train_response(station_code)


__all__ = [
    "app",
    "health",
    "search_stations",
    "live_bus",
    "live_train",
    "resolve_stop_id",
]