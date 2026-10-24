from pydantic import BaseModel, Field
from datetime import date


class ScheduleResponse(BaseModel):
    schedule_id: int
    student_subjects_id: int
    date: date
    pair_count: int


class ScheduleCreate(BaseModel):
    student_subjects_id: int = Field(gt=0)
    date: date
    pair_count: int = Field(ge=1)


class ScheduleUpdate(BaseModel):
    date: date
    pair_count: int = Field(ge=1)
 