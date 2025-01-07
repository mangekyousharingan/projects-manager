from src.core.entities.project import Project
from src.core.ports.project_repository import ProjectRepositoryPort


class ProjectService:
    def __init__(self, repository: ProjectRepositoryPort) -> None:
        self.repository = repository

    async def get_project_by_id(self, project_id: int) -> Project:
        project = await self.repository.get_project_by_id(project_id)

        if project is None:
            raise ValueError(f"Project with ID {project_id} not found")

        return Project(
            id=project.id,
            name=project.name,
            description=project.description,
            start_date=project.start_date,
            end_date=project.end_date,
            area_of_interest=project.area_of_interest,
        )

    async def create_project(self, project: Project) -> Project:
        project = await self.repository.create_project(project)

        return Project(
            id=project.id,
            name=project.name,
            description=project.description,
            start_date=project.start_date,
            end_date=project.end_date,
            area_of_interest=project.area_of_interest,
        )

    async def list_projects(self) -> list[Project]:
        return await self.repository.list_projects()

    async def delete_project(self, project_id: int) -> None:
        result = await self.repository.delete_project(project_id)

        if not result:
            raise ValueError(f"Project with ID {project_id} not found")

    async def update_project(self, project_id: int, project: Project) -> Project:
        updated_project = await self.repository.update_project(project_id, project)

        if updated_project is None:
            raise ValueError(f"Project with ID {project_id} not found")

        return Project(
            id=updated_project.id,
            name=updated_project.name,
            description=updated_project.description,
            start_date=updated_project.start_date,
            end_date=updated_project.end_date,
            area_of_interest=updated_project.area_of_interest,
        )
