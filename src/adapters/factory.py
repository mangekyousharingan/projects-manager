from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.database.factory import get_project_repository
from src.adapters.database.session import get_db_session
from src.core.services.project_service import ProjectService


def get_project_service(session: AsyncSession = Depends(get_db_session)) -> ProjectService:
    repository = get_project_repository(session)
    return ProjectService(repository)
