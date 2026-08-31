"""
Utility helpers for reading local GTFS static data files.

This module resolves files under apps/api/data/gtfs and exposes simple exact
and partial-match lookups for stops and routes.
"""

import csv
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data" / "gtfs"


def read_csv_rows(filename: str):
    """Read a GTFS CSV file into a list of dictionaries."""
    file_path = DATA_DIR / filename
    with open(file_path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def find_by_exact_field(filename: str, field_name: str, value: str):
    """Return rows whose field exactly matches the given value."""
    matches = []
    for row in read_csv_rows(filename):
        if row.get(field_name) == value:
            matches.append(row)
    return matches


def find_by_partial_field(filename: str, field_name: str, query: str):
    """Return rows whose field contains the query string, case-insensitive."""
    matches = []
    query_lower = query.lower()
    for row in read_csv_rows(filename):
        field_value = row.get(field_name, "") or ""
        if query_lower in field_value.lower():
            matches.append(row)
    return matches


def find_stop_by_code(stop_code: str):
    """Find stops by their public-facing stop code."""
    return find_by_exact_field("stops.txt", "stop_code", stop_code)


def find_stop_by_name(name_query: str):
    """Find stops by a partial, case-insensitive stop name match."""
    return find_by_partial_field("stops.txt", "stop_name", name_query)


def find_route_by_id(route_id: str):
    """Find a route by its GTFS route_id."""
    return find_by_exact_field("routes.txt", "route_id", route_id)


def find_route_by_short_name(short_name: str):
    """Find routes by their display number such as 120 or 126."""
    return find_by_exact_field("routes.txt", "route_short_name", short_name)


def find_route_by_name(name_query: str):
    """Find routes by a partial, case-insensitive route name match."""
    return find_by_partial_field("routes.txt", "route_long_name", name_query)