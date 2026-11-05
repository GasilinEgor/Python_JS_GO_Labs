from pydantic import BaseModel, ConfigDict


class StudentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: int
    username: str


class StudentAverageResponse(BaseModel):
    student_id: int
    average_grade: float | None
    marks_count: int


class StudentListResponse(BaseModel):
    students: list[StudentResponse]
    total: int
