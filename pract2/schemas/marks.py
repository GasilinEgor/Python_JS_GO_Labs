from pydantic import BaseModel, Field


class MarksResponse(BaseModel):
    marks_id: int
    student_subject_id: int
    mark: int


class MarkCreate(BaseModel):
    student_subject_id: int = Field(gt=0)
    mark: int = Field(ge=2, le=5)


class MarkUpdate(BaseModel):
    mark: int = Field(ge=2, le=5)
