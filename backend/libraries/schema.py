from ninja import Schema

class ReadLibraryOccupancy(Schema):
    library_name: str
    occupancy_percentage: float
    last_updated: str
    