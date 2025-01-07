import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.database.tables.project import ProjectTable
from src.core.entities.project import Project
from src.core.ports.project_repository import ProjectRepositoryPort

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProjectRepository(ProjectRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_project_by_id(self, project_id: int) -> Project | None:
        async with self.session as session:
            query = select(ProjectTable).where(ProjectTable.id == project_id)
            result = await session.execute(query)
            project_table = result.scalar_one_or_none()

            if project_table is None:
                return None

            return Project(
                id=project_table.id,
                name=project_table.name,
                description=project_table.description,
                start_date=project_table.start_date,
                end_date=project_table.end_date,
                area_of_interest=project_table.area_of_interest,
            )

    async def create_project(self, project: Project) -> Project:
        async with self.session as session:
            new_project = ProjectTable(
                name=project.name,
                description=project.description,
                start_date=project.start_date,
                end_date=project.end_date,
                area_of_interest=project.area_of_interest,
            )

            session.add(new_project)
            await session.commit()
            await session.refresh(new_project)

            project.id = new_project.id

            return project

    async def list_projects(self) -> list[Project]:
        async with self.session as session:
            query = select(ProjectTable)
            result = await session.execute(query)
            project_tables = result.scalars().all()

            return [
                Project(
                    id=project_table.id,
                    name=project_table.name,
                    description=project_table.description,
                    start_date=project_table.start_date,
                    end_date=project_table.end_date,
                    area_of_interest=project_table.area_of_interest,
                )
                for project_table in project_tables
            ]

    async def delete_project(self, project_id: int) -> bool:
        async with self.session as session:
            query = select(ProjectTable).where(ProjectTable.id == project_id)
            result = await session.execute(query)
            project_table = result.scalar_one_or_none()

            if project_table is None:
                return False

            await session.delete(project_table)
            await session.commit()

            return True

    async def update_project(self, project_id: int, updated_project: Project) -> Project | None:
        async with self.session as session:
            query = select(ProjectTable).where(ProjectTable.id == project_id)
            result = await session.execute(query)
            project_table = result.scalar_one_or_none()

            if project_table is None:
                return None

            project_table.name = updated_project.name
            project_table.description = updated_project.description
            project_table.start_date = updated_project.start_date
            project_table.end_date = updated_project.end_date
            project_table.area_of_interest = updated_project.area_of_interest

            await session.commit()
            await session.refresh(project_table)

            return Project(
                id=project_table.id,
                name=project_table.name,
                description=project_table.description,
                start_date=project_table.start_date,
                end_date=project_table.end_date,
                area_of_interest=project_table.area_of_interest,
            )
