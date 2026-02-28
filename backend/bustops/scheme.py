from ninja import Schema

class ReadBusStop(Schema):
    ATCOCode: str
    common_name: str
    indicator: str
    latitude: str
    longitude: str
    active: str

