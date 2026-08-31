import os

import certifi
import requests
from google.transit import gtfs_realtime_pb2

# GTFS Realtime Trip Updates API endpoint
GTFSR_URL = "https://api.nationaltransport.ie/gtfsr/v2/TripUpdates"
API_KEY = os.environ.get("NTA_API_KEY")


def get_upcoming_arrivals(stop_id: str):
    """
    Retrieve upcoming GTFS-Realtime bus arrivals for a specific stop_id.

    This function is intentionally low-level: it expects the GTFS internal
    stop_id, not the user-facing stop number or stop name.
    """
    if not API_KEY:
        raise RuntimeError("NTA_API_KEY is not configured.")

    headers = {"x-api-key": API_KEY}
    resp = requests.get(GTFSR_URL, headers=headers, timeout=10, verify=certifi.where())
    resp.raise_for_status()

    # Parse protobuf binary data into Python objects
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(resp.content)

    arrivals = []
    for entity in feed.entity:
        if not entity.HasField("trip_update"):
            continue

        trip = entity.trip_update
        for stu in trip.stop_time_update:
            if stu.stop_id != stop_id:
                continue

            arrival_ts = stu.arrival.time if stu.HasField("arrival") else None
            arrivals.append(
                {
                    "route_id": trip.trip.route_id,
                    "trip_id": trip.trip.trip_id,
                    "arrival_unix": arrival_ts,
                    "delay_secs": stu.arrival.delay if stu.HasField("arrival") else None,
                }
            )

    return sorted(arrivals, key=lambda x: x["arrival_unix"] or 0)