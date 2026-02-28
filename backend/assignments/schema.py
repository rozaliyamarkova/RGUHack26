from ninja import Schema


class CreateAssignment(Schema):
    title: str
    due_date: str
    time_needed:int
    weighting: float|None = None
    grade: float|None = None
    
class ReadAssignment(Schema):
    id: int
    title: str
    due_date: str
    time_needed:int
    time_estimated:int|None = None
    weighting: float|None = None
    grade: float|None = None

class UpdateAssignment(Schema):
    title: str|None = None
    due_date: str|None = None
    time_needed:int|None = None
    weighting: float|None = None
    grade: float|None = None

class CreateAssignmentLog(Schema):
    duration: int|None = None
    notes: str|None = None

class ReadAssignmentLog(Schema):
    id: int
    duration: int|None = None
    notes: str|None = None
    created_at: str