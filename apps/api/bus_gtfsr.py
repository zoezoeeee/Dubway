import os
import requests
from google.transit import gtfs_realtime_pb2

GTFSR_URL = "https://api.nationaltransport.ie/gtfsr/v2/TripUpdates"
API_KEY = os.environ.get("NTA_API_KEY", "")


def get_upcoming_arrivals(stop_id: str):
    if not API_KEY:
        raise RuntimeError("NTA_API_KEY is not configured. Create an API subscription in the NTA developer portal.")

    headers = {"x-api-key": API_KEY}
    resp = requests.get(GTFSR_URL, headers=headers, timeout=10)
    resp.raise_for_status()

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
            arrivals.append({
                "route_id": trip.trip.route_id,
                "trip_id": trip.trip.trip_id,
                "arrival_unix": arrival_ts,
                "delay_secs": stu.arrival.delay if stu.HasField("arrival") else None,
            })
    return sorted(arrivals, key=lambda x: x["arrival_unix"] or 0)