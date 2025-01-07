from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.database.repository import ProjectRepository
from src.core.ports.project_repository import ProjectRepositoryPort


def get_project_repository(session: AsyncSession) -> ProjectRepositoryPort:
    return ProjectRepository(session)
