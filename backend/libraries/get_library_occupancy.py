import requests
import time
import json


def get_library_occupancy_helper(library_slug):
    if library_slug in LIBRARIES:
        return LIBRARIES[library_slug]["function"]()

def get_sdr_occupancy():
    response = requests.get("https://www.ricecube.live/api/samples/sir_duncan_rice/day")
    response.raise_for_status()

    data = json.loads(response.content)["previous"][-1]

    return {
        "library_name": "Sir Duncan Rice Library",
        "occupancy_percentage": data[2],
        "last_updated": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(data[1])))
    }

LIBRARIES = {
    "sdr": {
        "function": get_sdr_occupancy
    }
}