from ninja import Schema

class ReadBusStop(Schema):
    ATCOCode: str
    common_name: str
    indicator: str
    latitude: str
    longitude: str
    active: str

class Bus(Schema):
    line: str
    direction: str
    operator: str
    scheduled_time: str
    departure_time: str
    is_realtime: bool
