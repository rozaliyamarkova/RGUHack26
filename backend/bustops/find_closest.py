import pandas as pd
from lat_lon_parser import parse
import json
from bustops.models import BusStop


def load_data(closest):
    lis = []
    for close_stop in closest:
        lis.append(BusStop.objects.get(ATCOCode = close_stop[0]))

    return lis

        


def find_closest_bus_stops(user_lattitude, user_longitude):
    user_lattitude = parse(user_lattitude)
    user_longitude = parse(user_longitude)

    busstops = BusStop.objects.all()

    bus_difference = []

    for question in busstops:
        stop_longitude = float(question.longitude)
        stop_lattitude = float(question.latitude)

        ATCOCode = question.ATCOCode

        longitude_difference = abs(user_longitude - stop_longitude)
        lattitude_difference = abs(user_lattitude - stop_lattitude)

        total_difference = (longitude_difference**2 + lattitude_difference**2)**0.5

        bus_difference.append([ATCOCode, total_difference])
        


    
    bus_difference.sort(key=lambda x: x[1])
    n=5
    closest_n = bus_difference[0:n]

    closest = load_data(closest_n)
    
    return closest
    