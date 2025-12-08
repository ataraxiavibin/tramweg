# tramweg.py
#
# 1. get a station
# 2. make a request to the api
# 3. list the info

from rich import print
import requests
import json
from datetime import datetime

BASE_LINK = "https://v6.vbb.transport.rest"

def main():
    print("-" * 50)
    user_station = input("What station?\n").lower()

    data = requests.get(f"{BASE_LINK}/locations?query={user_station} berlin&results=1").json()
    station_name = data[0]["name"]
    station_id = data[0]["id"]

    # only show departures in ten minutes
    departures_data = requests.get(f"{BASE_LINK}/stops/{station_id}/departures?duration=10").json()

    if not departures_data['departures']:
        raise Exception("No departures found.")

    print(f"\n[bold]Departures from {station_name}: [/bold]")

    try:
        for trip in departures_data['departures']:
            line_name = trip['line']['name'] 
            
            direction = trip['direction']
            
            when = trip['when'] # ISO format

            if when is None:
                print("skipped some " + line_name)
                continue

            # making it readable
            departure_time = datetime.fromisoformat(when)
            now = datetime.now().astimezone()
            delta = departure_time - now

            minutes_left = int(delta.total_seconds() / 60)

            # output
            if minutes_left < 0:
                print(f"[{line_name}] -> {direction} | left {minutes_left} minutes ago.")
            elif minutes_left == 0:
                print(f"[{line_name}] -> {direction} | departing right now.")
            else:
                print(f"[{line_name}] -> {direction} | in {minutes_left} minutes.")

    except Exception as e:
        # very useful
        print(f"something went wrong: {e}")



if __name__ == "__main__":
    main()
