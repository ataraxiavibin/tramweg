# tramweg.py
# SPDX-License-Identifier: GPL-3.0-only

from rich.console import Console
from rich.table import Table
from rich import box 
import requests
import json
from datetime import datetime

BASE_LINK = "https://v6.vbb.transport.rest"
CACHE_FILE = "station_cache.json"

def load_cache() -> dict:
    with open(CACHE_FILE, "r") as file:
        cache = json.load(file)

    return cache


def dump_cache(cache: dict) -> None:
    with open(CACHE_FILE, "w") as file:
        json.dump(cache, file)


def get_station_id(user_input: str, cache: dict) -> tuple[str, str, dict]:
    if user_input in cache:
        station_name = cache[user_input]["name"]
        station_id = cache[user_input]["id"]
    else:
        data = requests.get(f"{BASE_LINK}/locations?query={user_input} berlin&results=1",timeout=5).json()
        station_name = data[0]["name"]
        station_id = data[0]["id"]

        cache[user_input] = {"id": station_id, "name": station_name}

    return (station_name, station_id, cache)


def get_departures(station_id: str) -> dict:
    return requests.get(f"{BASE_LINK}/stops/{station_id}/departures?duration=10", timeout=5).json() # only 10 last departures


def calculate_time_left(iso_date: str) -> int:
    departure_time = datetime.fromisoformat(iso_date)
    now = datetime.now().astimezone()
    delta = departure_time - now

    return int(delta.total_seconds() / 60)


def main() -> None:
    try:
        cache = load_cache()
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        cache = {}

    print("-" * 50)
    user_station = input("What station?\n").lower().strip()

    station_name, station_id, cache = get_station_id(user_station, cache)
    dump_cache(cache)

    departures_data = get_departures(station_id)

    if not departures_data['departures']:
        raise Exception("No departures found.")

    console = Console()
    table = Table(title=f"Abfahrten {station_name}", style="orange_red1", header_style="bold orange_red1", box=box.SIMPLE, show_lines=False)

    table.add_column("Linie", style="bold white", justify="left", width=5)
    table.add_column("Ziel", style="orange_red1")
    table.add_column("Abfahrt", style="bold orange_red1", justify="right")

    try:
        for trip in departures_data['departures']:
            line_name = trip['line']['name'] 
            direction = trip['direction']

            if (when := trip['when']) is None: continue

            minutes_left = calculate_time_left(when)

            if minutes_left < 0:
                time_str = "weg"
            elif minutes_left == 0:
                time_str = "sofort"
            else:
                time_str = f"{minutes_left} min"

            table.add_row(line_name, direction, time_str)

        console.print(table)

    except Exception as e:
        print(f"[red]something went wrong: {e}[/red]")


if __name__ == "__main__":
    main()
