from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
import logging
import os

from fastapi import FastAPI
from psycopg2 import OperationalError
from sqlalchemy import create_engine, text

from src.adapters.fastapi.api import api_router

# TODO: Added temporary testing
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# TODO: Added temporary for testing
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

engine = create_engine(DATABASE_URL)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Database connection successful!")
    except OperationalError as e:
        logger.info(f"Database connection failed: {str(e)}")
        raise RuntimeError("Failed to connect to the database") from e

    yield

    logger.info("Application is shutting down...")


app = FastAPI(title="Projects manager API", lifespan=lifespan)

app.include_router(router=api_router)
