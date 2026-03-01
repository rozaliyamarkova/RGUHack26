import requests
import time
import json

rgu_floor_capacity = {
    'Library Level 6': 128,
    'Library Level 7': 139,
    'Library Level 8': 139,
    'Library Level 9': 324,
}

def get_library_occupancy_helper(library_slug):
    if library_slug in LIBRARIES:
        return LIBRARIES[library_slug]["function"]()

def get_sdr_occupancy():
    response = requests.get("https://www.ricecube.live/api/samples/sir_duncan_rice/day")
    response.raise_for_status()

    data = json.loads(response.content)["previous"][-1]

    print(data)

    return {
        "library_name": "Sir Duncan Rice Library",
        "occupancy_percentage": data[2],
        "last_updated": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(data[1])))
    }

def get_rgu_occupancy():
    response = requests.get("https://spaces.rgu.ac.uk/api/groups/library/feed")
    response.raise_for_status()
    data = response.json()["data"]

    floors = []
    for floor in data:
        capacity = rgu_floor_capacity.get(floor["name"], 100)
        percentage = round((floor["current_usage"] / capacity) * 100)
        floors.append({
            "name": floor["name"],
            "current_usage": floor["current_usage"],
            "capacity": capacity,
            "occupancy_percentage": percentage,
            "status": floor["status"]
        })

    return {
        "library_name": "RGU Library",
        "floors": floors,
        "last_updated": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    }



LIBRARIES = {
    "sdr": {
        "function": get_sdr_occupancy
    },
    "rgu": { "function": get_rgu_occupancy }
}