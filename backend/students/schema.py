from ninja import Schema


class CreateStudent(Schema):
    name: str

class ReadStudent(Schema):
    name: str