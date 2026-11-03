from fastapi import APIRouter, Depends, HTTPException, status

from database.connection import get_db
from database.models import User, Role, StudentSubjects, Marks

from core.dependencies import get_target_student, require_teacher

from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from schemas.student import StudentResponse, StudentAverageResponse, StudentListResponse


router = APIRouter(prefix="/student", tags=['Students'])


@router.get("/{student_id}/average", response_model=StudentAverageResponse)
def get_student_average(target: User = Depends(get_target_student), db: Session = Depends(get_db)):
    try:
        query = (select(func.avg(Marks.mark), func.count(Marks.marks_id)).join(StudentSubjects, Marks.student_subjects_id == StudentSubjects.student_subjects_id).where(StudentSubjects.student_id == target.student_id))
        average, marks_count = db.execute(query).one()

        return StudentListResponse(student_id=target.user_id, average_grade=(round(float(average), 2) if average is not None else None), marks_count=marks_count)
    
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="У него ничего нет")


@router.get("/all", response_model=StudentListResponse)
def get_all_students(teacher: User = Depends(require_teacher), db: Session = Depends(get_db)):
    try:
        query = (select(User).join(Role, User.role_id == Role.role_id).where(func.lower(Role.role_name) == 'student').order_by(User.user_id))
        students = db.scalars(query).all()

        return StudentListResponse(students=[StudentResponse.model_validate(student) for student in students], total=len(students))

    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail='Дата база вынесена')

