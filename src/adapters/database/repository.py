from src.core.entities.project import Project
from src.core.ports.project_repository import ProjectRepositoryPort


class ProjectRepository(ProjectRepositoryPort):
    def get_project(self, project_id: int) -> Project:
        pass

    def create_project(self) -> Project:
        pass
