from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.database.repository import ProjectRepository


def get_project_repository(session: AsyncSession) -> ProjectRepository:
    return ProjectRepository(session)
