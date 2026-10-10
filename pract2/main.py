from fastapi import FastAPI
from contextlib import asynccontextmanager

import logging

from alembic import command
from alembic.config import Config

from database.seed import seed_database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Применение миграций Alembic")
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    logger.info("Инициализация стандартных данных")
    seed_database()
    logger.info("Всё готово, поставьте 5 пж")
    yield

app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello World"}