from pydantic import BaseModel, ConfigDict, Field


class MarksResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    marks_id: int
    student_subjects_id: int
    mark: int


class MarkCreate(BaseModel):
    student_subjects_id: int = Field(gt=0)
    mark: int = Field(ge=2, le=5)


class MarkUpdate(BaseModel):
    mark: int = Field(ge=2, le=5)
