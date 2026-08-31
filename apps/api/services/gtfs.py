import time
from typing import Optional

from fastapi import HTTPException

from bus_gtfsr import get_upcoming_arrivals
from gtfs_lookup import find_stop_by_code, find_stop_by_name
from irish_rail import find_station_code, get_station_trains

bus_cache: dict[str, tuple[list[dict], float]] = {}
CACHE_TTL_SECONDS = 20


def resolve_stop_id(query: str) -> str:
    """
    Resolve a user-facing stop query into the GTFS stop_id.
    The query may be either a stop number (e.g. '842') or a stop name
    (e.g. 'Abbey Street').
    """
    stop_code_query = query.strip()

    stop_matches = find_stop_by_code(stop_code_query)
    if stop_matches:
        return stop_matches[0]["stop_id"]

    stop_matches = find_stop_by_name(stop_code_query)
    if stop_matches:
        return stop_matches[0]["stop_id"]

    raise HTTPException(status_code=404, detail=f"Stop not found for query: {query}")


def search_station_code(query: str):
    return find_station_code(query)


def get_live_bus_response(query: str):
    try:
        stop_id = resolve_stop_id(query)
    except HTTPException:
        raise

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


def get_live_train_response(station_code: str):
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
