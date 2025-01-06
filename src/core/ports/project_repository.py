from abc import ABC, abstractmethod

from src.core.entities.project import Project


class ProjectRepositoryPort(ABC):
    @abstractmethod
    def get_project(self, project_id: int) -> Project:
        pass

    @abstractmethod
    def create_project(self) -> Project:
        pass
