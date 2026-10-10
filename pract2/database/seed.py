import secrets
import logging

from pwdlib import PasswordHash
from sqlalchemy import select

from database.connection import Session
from database.models import User, Role

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

INITIAL_ROLES = ('Teacher', 'Student')
INITIAL_USERS = (("teacher1", 'Teacher'),
                 ("teacher2", 'Teacher'),
                 ("student1", 'Student'),
                 ("student2", 'Student'))

password_hasher = PasswordHash.recommended()


def seed_database():
    logger.info("Начинаем инициализацию начальных данных")
    # остальной код функции
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
            user = User(username=username, 
                        role_id=roles_name[user_role].role_id,
                        password=password_hash)
            session.add(user)

            new_users.append((username, password))
            existing_users.add(username)
    
    for username, password in new_users:
        logger.warning(
            f"Создан новый аккаунт: {username}, {password}"
        )
    
    logger.info("Инициализация прошла успешно!")

