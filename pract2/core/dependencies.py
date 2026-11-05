from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from core.security import decode_token
from database.connection import get_db
from database.models import Role, User

bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    try:
        payload = decode_token(credentials.credentials, "access")
        user_id = int(payload["sub"])
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недействительный или просроченный access-токен",
            headers={"WWW-Authenticate": "Bearer"},
        ) from err

    user = db.get(User, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден",
        )

    return user


def require_teacher(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> User:

    role = db.get(Role, current_user.role_id)

    if role is None or role.role_name.lower() != "teacher":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Операция доступна только преподавателю",
        )

    return current_user


def get_target_student(
    student_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    role = db.get(Role, current_user.role_id)

    if role is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Роль не определена"
        )

    role_name = role.role_name.lower()

    # Если авторизован студент
    if role_name == "student":
        if student_id != "self":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Не подглядывай за другими!",
            )

        return current_user

    # Если авторизован преподаватель
    if role_name == "teacher":
        if student_id == "self":
            return current_user

        try:
            target_id = int(student_id)
        except ValueError as err:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Неправильный ввод",
            ) from err

        if target_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Неправильный ввод",
            )

        student = db.get(User, target_id)

        if student is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Студент не существует",
            )

        student_role = db.get(Role, student.role_id)

        if student_role is None or student_role.role_name.lower() != "student":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Нет такого студента",
            )

        return student

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Доступ запрещён"
    )
