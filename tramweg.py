# tramweg.py
#
# 1.
# [x] get a station
# [x] make a request to the api
# [x] list the info
#
# 2. 
# [x] store the ids in the cache file
# [ ] fuzzy check if the name of the station is in the cache file
# [ ] (optional) make it fucking readable
#
# 3.
# [x] add more Berlin-ish look to the CLI output


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


def dump_cache(cache) -> None:
    with open(CACHE_FILE, "w") as file:
        json_string = json.dump(cache, file)


def main():
    try:
        cache = load_cache()
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        cache = {}

    print("-" * 50)
    user_station = input("What station?\n")

    if user_station in cache:
        station_name = cache[user_station]["name"]
        station_id = cache[user_station]["id"]
        departures_data = requests.get(f"{BASE_LINK}/stops/{station_id}/departures?duration=10").json()
        print("in the cache")
    else:
        data = requests.get(f"{BASE_LINK}/locations?query={user_station} berlin&results=1").json()
        station_name = data[0]["name"]
        station_id = data[0]["id"]

        cache[user_station] = {"id": station_id, "name": station_name}
        dump_cache(cache)
        departures_data = requests.get(f"{BASE_LINK}/stops/{station_id}/departures?duration=10").json()
        print("API id")

    if not departures_data['departures']:
        raise Exception("No departures found.")


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
            when = trip['when'] # ISO format

            if when is None:
                continue

            # ISO -> readable
            departure_time = datetime.fromisoformat(when)
            now = datetime.now().astimezone()
            delta = departure_time - now
            minutes_left = int(delta.total_seconds() / 60)

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
