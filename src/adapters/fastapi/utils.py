from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import Request, FastAPI
from psycopg2 import OperationalError
from sqlalchemy import text
from starlette.responses import JSONResponse

from src.adapters.database.session import sessionmanager


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    print(f"Unhandled exception occurred: {exc}")

    error_details = {
        "message": "An internal server error occurred. Please try again later.",
        "error_type": type(exc).__name__,
        "details": str(exc),
        "path": request.url.path,
    }

    return JSONResponse(
        status_code=500,
        content=error_details,
    )


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    try:
        async with sessionmanager.session() as session:
            await session.execute(text("SELECT 1"))
        print("Database connection successful!")
    except OperationalError as e:
        print(f"Database connection failed: {str(e)}")
        raise RuntimeError("Failed to connect to the database") from e

    yield

    print("Application is shutting down...")
