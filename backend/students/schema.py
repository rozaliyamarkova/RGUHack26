from ninja import Schema


class CreateStudent(Schema):
    name: str

class ReadStudent(Schema):
    name: str
    user_id:str