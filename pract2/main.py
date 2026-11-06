import logging
from contextlib import asynccontextmanager

from alembic.config import Config
from fastapi import FastAPI

from alembic import command
from database.seed import add_test_users, create_test_subjects, seed_database
from routers.disciplines import router as desciplines_router
from routers.session import router as session_router
from routers.student import router as student_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Применение миграций Alembic")
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    logger.info("Инициализация стандартных данных")
    seed_database()
    create_test_subjects()
    add_test_users()
    logger.info("Всё готово, поставьте 5 пж")
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(session_router)
app.include_router(desciplines_router)
app.include_router(student_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
