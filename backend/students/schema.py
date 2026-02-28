from uuid import UUID

from ninja import Schema


class CreateStudent(Schema):
    name: str

class CreateStudentResponse(Schema):
    name: str
    user_id:UUID

class ReadStudent(Schema):
    name: str