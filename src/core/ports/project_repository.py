from abc import ABC, abstractmethod

from src.core.entities.project import Project


class ProjectRepositoryPort(ABC):
    @abstractmethod
    async def get_project_by_id(self, project_id: int) -> Project | None:
        pass

    @abstractmethod
    async def create_project(self, project: Project) -> Project:
        pass

    @abstractmethod
    async def list_projects(self) -> list[Project]:
        pass

    @abstractmethod
    async def delete_project(self, project_id: int) -> bool:
        pass

    @abstractmethod
    async def update_project(self, project_id: int, updated_project: Project) -> Project | None:
        pass
