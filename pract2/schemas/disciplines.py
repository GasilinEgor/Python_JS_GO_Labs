from pydantic import BaseModel, Field

class DisciplineCreate(BaseModel):
    subject_id: int = Field(gt=0)

class DisciplineUpdate(BaseModel):
    subject_id: int = Field(gt=0)

class DisciplineResponse(BaseModel):
    student_id: int
    student_subjects_id: int
    subject_id: int
    subject_name: str
