import logging
import secrets

from pwdlib import PasswordHash
from sqlalchemy import select

from database.connection import Session
from database.models import Role, UniversitySubjects, User

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

INITIAL_ROLES = ("Teacher", "Student")
INITIAL_USERS = (
    ("teacher1", "Teacher"),
    ("teacher2", "Teacher"),
    ("student1", "Student"),
    ("student2", "Student"),
)

password_hasher = PasswordHash.recommended()


def seed_database():
    logger.info("Начинаем инициализацию начальных данных")
    new_users = []

    with Session.begin() as session:
        roles = session.scalars(select(Role)).all()
        roles_name = {role.role_name: role for role in roles}

        for role_name in INITIAL_ROLES:
            if role_name not in roles_name:
                role = Role(role_name=role_name)
                session.add(role)
                roles_name[role_name] = role

        session.flush()

        existing_users = set(session.scalars(select(User.username)).all())
        for username, user_role in INITIAL_USERS:
            if username in existing_users:
                continue

            password = secrets.token_urlsafe(16)
            password_hash = password_hasher.hash(password)
            user = User(
                username=username,
                role_id=roles_name[user_role].role_id,
                password=password_hash,
            )
            session.add(user)

            new_users.append((username, password))
            existing_users.add(username)

    for username, password in new_users:
        logger.warning(f"Создан новый аккаунт: {username}, {password}")

    logger.info("Инициализация прошла успешно!")


def add_test_users():
    users = {
        "my_student": User(
            username="teach1",
            role_id=1,
            password=password_hasher.hash("12345678"),
        ),
    }

    with Session.begin() as session:
        for user in users.values():
            session.add(user)


def create_test_subjects():
    subjects = ("ВЯП", "ВышМат", "МБП", "ДропБД")
    with Session.begin() as session:
        existing_subjects = set(
            session.scalars(select(UniversitySubjects.subject_name)).all()
        )
        for subject in subjects:
            if subject in existing_subjects:
                continue
            session.add(UniversitySubjects(subject_name=subject))
            existing_subjects.add(subject)
