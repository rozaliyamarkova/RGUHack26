from ninja import Schema

class CreateCourse(Schema):
    name:str

class ReadCourse(Schema):
    name:str