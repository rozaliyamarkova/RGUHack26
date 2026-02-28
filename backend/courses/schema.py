from ninja import Schema

class CreateCourse(Schema):
    name:str

class ReadCourse(Schema):
    id: int
    name:str

class UpdateCourse(Schema):
    name: str