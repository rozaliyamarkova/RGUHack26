from ninja import Schema
from datetime import datetime


class CreateAssignment(Schema):
    title: str
    due_date: datetime
    time_needed:int
    weighting: float|None = None
    grade: float|None = None
    
class ReadAssignment(Schema):
    id: int
    title: str
    due_date: datetime
    time_needed:int
    time_estimated:int|None = None
    weighting: float|None = None
    grade: float|None = None

class UpdateAssignment(Schema):
    title: str|None = None
    due_date: datetime|None = None
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