import csv
import sys
from pathlib import Path

STOPS_FILE = Path(__file__).parent / "data" / "gtfs" / "stops.txt"


def find_by_stop_code(stop_code: str):
    """Find stops by their public-facing stop number."""
    matches = []
    with open(STOPS_FILE, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("stop_code") == stop_code:
                matches.append(row)
    return matches


def find_by_name(name_query: str):
    """Find stops by a case-insensitive partial stop name."""
    matches = []
    name_query_lower = name_query.lower()
    with open(STOPS_FILE, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if name_query_lower in row.get("stop_name", "").lower():
                matches.append(row)
    return matches
