from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from core.dependencies import (
    get_current_user,
    get_target_student,
    require_teacher,
)
from database.connection import get_db
from database.models import (
    Marks,
    Role,
    StudentSchedule,
    StudentSubjects,
    UniversitySubjects,
    User,
)
from schemas.disciplines import (
    DisciplineCreate,
    DisciplineResponse,
    DisciplineUpdate,
)
from schemas.marks import MarkCreate, MarksResponse, MarkUpdate
from schemas.schedule import ScheduleCreate, ScheduleResponse, ScheduleUpdate

router = APIRouter(prefix="/disciplines", tags=["Disciplines"])


def require_role(role_name: str):
    def checker(
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
    ):
        role = db.get(Role, user.role_id)
        if role is None or role.role_name.lower() != role_name.lower():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для выполнения операции",
            )
        return user

    return checker


def get_student_subject(
    db: Session,
    student_id: int,
    student_subjects_id: int,
) -> StudentSubjects:
    association = db.scalar(
        select(StudentSubjects).where(
            StudentSubjects.student_subjects_id == student_subjects_id,
            StudentSubjects.student_id == student_id,
        )
    )

    if association is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Дисциплина студента не найдена",
        )

    return association


@router.get("/{student_id}", response_model=list[DisciplineResponse])
def get_disciplines(
    student_id: str,
    target: User = Depends(get_target_student),
    db: Session = Depends(get_db),
):
    try:
        query = (
            select(
                StudentSubjects.student_id,
                StudentSubjects.student_subjects_id,
                UniversitySubjects.subject_id,
                UniversitySubjects.subject_name,
            )
            .join(
                UniversitySubjects,
                StudentSubjects.subject_id == UniversitySubjects.subject_id,
            )
            .where(StudentSubjects.student_id == target.user_id)
            .order_by(UniversitySubjects.subject_name)
        )
        rows = db.execute(query).all()

        return [
            DisciplineResponse(
                student_id=row.student_id,
                student_subjects_id=row.student_subjects_id,
                subject_id=row.subject_id,
                subject_name=row.subject_name,
            )
            for row in rows
        ]

    except SQLAlchemyError as err:
        raise HTTPException(
            status_code=500, detail="Ошибка запроса дисциплин"
        ) from err


@router.post(
    "/{student_id}",
    response_model=DisciplineResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_discipline(
    student_id: str,
    data: DisciplineCreate,
    db: Session = Depends(get_db),
    target: User = Depends(get_target_student),
    teacher: User = Depends(require_teacher),
):
    try:
        subject = db.get(UniversitySubjects, data.subject_id)
        if subject is None:
            raise HTTPException(status_code=404, detail="Предмет не найден")

        existing = db.scalar(
            select(StudentSubjects).where(
                StudentSubjects.student_id == target.user_id,
                StudentSubjects.subject_id == data.subject_id,
            )
        )
        if existing is not None:
            raise HTTPException(status_code=409, detail="Предмет уже назначен")

        new_student_subject = StudentSubjects(
            student_id=target.user_id, subject_id=data.subject_id
        )
        db.add(new_student_subject)
        db.flush()

        res = DisciplineResponse(
            student_id=target.user_id,
            student_subjects_id=new_student_subject.student_subjects_id,
            subject_id=subject.subject_id,
            subject_name=subject.subject_name,
        )
        db.commit()
        return res

    except HTTPException:
        db.rollback()
        raise

    except IntegrityError as err:
        db.rollback()
        raise HTTPException(
            status_code=409, detail="Связь уже существует!"
        ) from err

    except SQLAlchemyError as err:
        db.rollback()
        raise HTTPException(
            status_code=500, detail="Ошибка БД (возможно, её дропнули)"
        ) from err


@router.put("/{student_id}/{discipline_id}", response_model=DisciplineResponse)
def update_discipline(
    discipline_id: int,
    data: DisciplineUpdate,
    target: User = Depends(get_target_student),
    teacher: User = Depends(require_teacher),
    db: Session = Depends(get_db),
):
    try:
        association = db.scalar(
            select(StudentSubjects).where(
                StudentSubjects.student_subjects_id == discipline_id,
                StudentSubjects.student_id == target.user_id,
            )
        )
        if association is None:
            raise HTTPException(status_code=404, detail="Запись не найдена")

        subject = db.get(UniversitySubjects, data.subject_id)
        if subject is None:
            raise HTTPException(status_code=404, detail="Предмет не найден")

        dublicate = db.scalar(
            select(StudentSubjects).where(
                StudentSubjects.student_id == target.user_id,
                StudentSubjects.subject_id == data.subject_id,
                StudentSubjects.student_subjects_id != discipline_id,
            )
        )
        if dublicate is not None:
            raise HTTPException(
                status_code=409,
                detail="Данная запись уже существует! Зачем редачить?",
            )

        association.subject_id = data.subject_id
        db.flush()

        result = DisciplineResponse(
            student_id=target.user_id,
            student_subjects_id=association.student_subjects_id,
            subject_id=subject.subject_id,
            subject_name=subject.subject_name,
        )
        db.commit()

        return result
    except HTTPException:
        db.rollback()
        raise

    except IntegrityError as err:
        db.rollback()
        raise HTTPException(
            status_code=409, detail="Нарушена целостность данных"
        ) from err

    except SQLAlchemyError as err:
        db.rollback()
        raise HTTPException(
            status_code=500, detail="Что-то с базой данных (её украли цыгане)"
        ) from err


@router.get("/{student_id}/grades", response_model=list[MarksResponse])
def get_grades(
    target: User = Depends(get_target_student), db: Session = Depends(get_db)
):
    try:
        query = (
            select(Marks)
            .join(
                StudentSubjects,
                Marks.student_subjects_id
                == StudentSubjects.student_subjects_id,
            )
            .where(StudentSubjects.student_id == target.user_id)
            .order_by(Marks.marks_id)
        )

        return list(db.scalars(query).all())

    except SQLAlchemyError as err:
        raise HTTPException(
            status_code=500, detail="Ошибка получени данных"
        ) from err


@router.post(
    "/{student_id}/grades",
    response_model=MarksResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_grade(
    data: MarkCreate,
    target: User = Depends(get_target_student),
    teacher: User = Depends(require_teacher),
    db: Session = Depends(get_db),
):
    try:
        get_student_subject(db, target.user_id, data.student_subjects_id)
        grade = Marks(
            student_subjects_id=data.student_subjects_id, mark=data.mark
        )
        db.add(grade)
        db.commit()
        db.refresh(grade)

        return grade
    except HTTPException:
        db.rollback()
        raise

    except SQLAlchemyError as err:
        db.rollback()
        raise HTTPException(
            status_code=500, detail="Данные теперь лежат в даркнете"
        ) from err


@router.put(
    "/{student_id}/grades/{grade_id}",
    response_model=MarksResponse,
)
def update_grade(
    grade_id: int,
    data: MarkUpdate,
    target: User = Depends(get_target_student),
    teacher: User = Depends(require_teacher),
    db: Session = Depends(get_db),
):
    try:
        grade = db.scalar(
            select(Marks)
            .join(
                StudentSubjects,
                Marks.student_subjects_id
                == StudentSubjects.student_subjects_id,
            )
            .where(
                Marks.marks_id == grade_id,
                StudentSubjects.student_id == target.user_id,
            )
        )

        if grade is None:
            raise HTTPException(
                status_code=404,
                detail="Такая оценка не найдена",
            )

        grade.mark = data.mark
        db.commit()
        db.refresh(grade)

        return grade

    except HTTPException:
        db.rollback()
        raise

    except SQLAlchemyError as err:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Ошибка при изменении оценки",
        ) from err


@router.get("/{student_id}/schedule", response_model=list[ScheduleResponse])
def get_schedule(
    target: User = Depends(get_target_student), db: Session = Depends(get_db)
):
    try:
        query = (
            select(StudentSchedule)
            .join(
                StudentSubjects,
                StudentSchedule.student_subjects_id
                == StudentSubjects.student_subjects_id,
            )
            .where(StudentSubjects.student_id == target.user_id)
            .order_by(StudentSchedule.date, StudentSchedule.pair_count)
        )
        return list(db.scalars(query).all())
    except SQLAlchemyError as err:
        raise HTTPException(
            status_code=500, detail="Расписание будет сделано когда-нибудь"
        ) from err


@router.post(
    "/{student_id}/disciplines",
    response_model=ScheduleResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_schedule(
    data: ScheduleCreate,
    target: User = Depends(get_target_student),
    teacher: User = Depends(require_teacher),
    db: Session = Depends(get_db),
):
    try:
        get_student_subject(db, target.user_id, data.student_subjects_id)
        lesson = StudentSchedule(
            student_subjects_id=data.student_subjects_id,
            date=data.date,
            pair_count=data.pair_count,
        )
        db.add(lesson)
        db.commit()
        db.refresh(lesson)
        return lesson

    except HTTPException:
        db.rollback()
        raise

    except IntegrityError as err:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Он не сможет ходить на 2 пары зара, он порвётся",
        ) from err

    except SQLAlchemyError as err:
        db.rollback()
        raise HTTPException(
            status_code=500, detail="Сервера МИРЭА легли от такого расписания"
        ) from err


@router.put(
    "/{student_id}/schedule/{schedule_id}", response_model=ScheduleResponse
)
def update_schedule(
    schedule_id: int,
    data: ScheduleUpdate,
    target: User = Depends(get_target_student),
    teacher: User = Depends(require_teacher),
    db: Session = Depends(get_db),
):
    try:
        lesson = db.scalar(
            select(StudentSchedule)
            .join(
                StudentSubjects,
                StudentSubjects.student_subjects_id
                == StudentSchedule.student_subjects_id,
            )
            .where(
                StudentSchedule.schedule_id == schedule_id,
                StudentSubjects.student_id == target.user_id,
            )
        )

        if lesson is None:
            raise HTTPException(
                status_code=404,
                detail="Ему повезло, что у него нет пар на это время",
            )

        lesson.date = data.date
        lesson.pair_count = data.pair_count

        db.commit()
        db.refresh(lesson)
        return lesson

    except HTTPException:
        db.rollback()
        raise

    except SQLAlchemyError as err:
        db.rollback()
        raise HTTPException(status_code=500, detail="Ой всё") from err
