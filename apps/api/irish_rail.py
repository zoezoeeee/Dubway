import requests
import xml.etree.ElementTree as ET

BASE_URL = "http://api.irishrail.ie/realtime/realtime.asmx"
NS = {"ns": "http://api.irishrail.ie/realtime/"}


def get_station_trains(station_code: str, num_mins: int = 90):
    url = f"{BASE_URL}/getStationDataByCodeXML_WithNumMins"
    resp = requests.get(url, params={"StationCode": station_code, "NumMins": num_mins}, timeout=10)
    resp.raise_for_status()
    root = ET.fromstring(resp.content)

    trains = []
    for obj in root.findall("ns:objStationData", NS):
        def text(tag):
            el = obj.find(f"ns:{tag}", NS)
            return el.text if el is not None else None

        trains.append({
            "destination": text("Destination"),
            "due_in_mins": text("Duein"),
            "expected_departure": text("Expdepart"),
            "scheduled_departure": text("Schdepart"),
            "status": text("Status"),
            "direction": text("Direction"),
        })
    return trains


def find_station_code(name_query: str):
    url = f"{BASE_URL}/getStationDataByNameXML"
    resp = requests.get(url, params={"StationDesc": name_query}, timeout=10)
    resp.raise_for_status()
    root = ET.fromstring(resp.content)
    results = []
    for obj in root.findall("ns:objStationData", NS):
        code = obj.find("ns:Stationcode", NS)
        desc = obj.find("ns:Stationfullname", NS)
        if code is not None:
            results.append((desc.text if desc is not None else "?", code.text))
    return results