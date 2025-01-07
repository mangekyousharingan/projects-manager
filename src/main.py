from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from psycopg2 import OperationalError
from sqlalchemy import text

from src.adapters.database.session import sessionmanager
from src.adapters.fastapi.api import api_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    try:
        async with sessionmanager.session() as session:
            await session.execute(text("SELECT 1"))
        logger.info("Database connection successful!")
    except OperationalError as e:
        logger.info(f"Database connection failed: {str(e)}")
        raise RuntimeError("Failed to connect to the database") from e

    yield

    logger.info("Application is shutting down...")


app = FastAPI(title="Projects manager API", lifespan=lifespan)

app.include_router(router=api_router)
