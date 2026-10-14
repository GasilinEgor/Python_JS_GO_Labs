from pydantic import BaseModel
from datetime import date


class CreateDiscipline(BaseModel):
    student_id: int
    subject_id: int

class ChangeDiscipline(BaseModel):
    student_id: int
    schedule_id: int
    date: date
    pair_count: int

class AddMark(BaseModel):
    student_id: int
    schedule_id: int
    mark: int

class SetSubjectSchedule(BaseModel):
    student_id: int
    subject_id: int
    date: date
    pair_count: int

class ChangeSubjectSchedule(BaseModel):
    student_id: int
    schedule_id: int
