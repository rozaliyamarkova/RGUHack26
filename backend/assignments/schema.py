from ninja import Schema


class CreateAssignment(Schema):
    title: str
    due_date: str
    time_needed:int
    weighting: float|None = None
    grade: float|None = None
    