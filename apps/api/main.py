import time
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from bus_gtfsr import get_upcoming_arrivals
from irish_rail import find_station_code, get_station_trains

load_dotenv()

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
    return find_station_code(q)


@app.get("/live/bus")
def live_bus(stop_id: str):
    now = time.time()
    cached = bus_cache.get(stop_id)

    if cached is not None:
        cached_arrivals, cached_at = cached
        if now - cached_at < CACHE_TTL_SECONDS:
            return format_bus_response(cached_arrivals)

    try:
        arrivals = get_upcoming_arrivals(stop_id)
        bus_cache[stop_id] = (arrivals, now)
        return format_bus_response(arrivals)
    except RuntimeError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=502, detail=str(error)) from error


@app.get("/live/train")
def live_train(station_code: str):
    try:
        arrivals = get_station_trains(station_code, num_mins=120)
        return format_train_response(arrivals)
    except Exception as error:
        raise HTTPException(status_code=502, detail=str(error)) from error


def format_bus_response(arrivals: list[dict]) -> dict:
    departures = []

    for arrival in arrivals[:3]:
        arrival_unix = arrival.get("arrival_unix")
        delay_seconds = arrival.get("delay_secs")

        departures.append(
            {
                "time": format_unix_time(arrival_unix),
                "minutesAway": minutes_until(arrival_unix),
                "status": "Delayed" if delay_seconds and delay_seconds > 60 else "On time",
            }
        )

    return {
        "source": "TFI Live",
        "updatedAt": int(time.time()),
        "departures": departures,
    }


def format_train_response(arrivals: list[dict]) -> dict:
    departures = []

    for arrival in arrivals[:3]:
        due_value = arrival.get("due_in_mins")
        due_minutes = int(due_value) if str(due_value).isdigit() else None

        departures.append(
            {
                "time": arrival.get("expected_departure") or "—",
                "minutesAway": due_minutes,
                "status": normalize_train_status(arrival.get("status")),
            }
        )

    return {
        "source": "Irish Rail",
        "updatedAt": int(time.time()),
        "departures": departures,
    }


def format_unix_time(unix_time: Optional[int]) -> str:
    if unix_time is None:
        return "—"
    return time.strftime("%H:%M", time.localtime(unix_time))


def minutes_until(unix_time: Optional[int]) -> Optional[int]:
    if unix_time is None:
        return None
    return max(0, round((unix_time - time.time()) / 60))


def normalize_train_status(status: Optional[str]) -> str:
    if status and "late" in status.lower():
        return "Delayed"
    return "On time"