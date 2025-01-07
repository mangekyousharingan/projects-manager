from datetime import date

import pytest
from unittest.mock import AsyncMock
from src.core.entities.project import Project
from src.core.services.project_service import ProjectService


@pytest.fixture
def mock_repository():
    """Fixture to create a mock repository."""
    return AsyncMock()


@pytest.fixture
def project_service(mock_repository):
    """Fixture to create a ProjectService instance with a mock repository."""
    return ProjectService(repository=mock_repository)


@pytest.fixture
def sample_project():
    return Project(
        id=1,
        name="Test Project",
        description="A test description",
        start_date=date(2025, 1, 1),
        end_date=date(2025, 12, 31),
        area_of_interest=None,  # Mock geometry can be added if needed
    )


@pytest.mark.asyncio
async def test_get_project_by_id(project_service, mock_repository, sample_project):
    mock_repository.get_project_by_id.return_value = sample_project

    project = await project_service.get_project_by_id(1)

    assert project.id == sample_project.id
    assert project.name == sample_project.name
    mock_repository.get_project_by_id.assert_awaited_once_with(1)


@pytest.mark.asyncio
async def test_get_project_by_id_not_found(project_service, mock_repository):
    mock_repository.get_project_by_id.return_value = None

    with pytest.raises(ValueError, match="Project with ID 1 not found"):
        await project_service.get_project_by_id(1)

    mock_repository.get_project_by_id.assert_awaited_once_with(1)


@pytest.mark.asyncio
async def test_create_project(project_service, mock_repository, sample_project):
    mock_repository.create_project.return_value = sample_project

    project = await project_service.create_project(sample_project)

    assert project.id == sample_project.id
    assert project.name == sample_project.name
    mock_repository.create_project.assert_awaited_once_with(sample_project)


@pytest.mark.asyncio
async def test_list_projects(project_service, mock_repository, sample_project):
    mock_repository.list_projects.return_value = [sample_project]

    projects = await project_service.list_projects()

    assert len(projects) == 1
    assert projects[0].id == sample_project.id
    mock_repository.list_projects.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_project(project_service, mock_repository):
    mock_repository.delete_project.return_value = True

    await project_service.delete_project(1)

    mock_repository.delete_project.assert_awaited_once_with(1)


@pytest.mark.asyncio
async def test_delete_project_not_found(project_service, mock_repository):
    mock_repository.delete_project.return_value = False

    with pytest.raises(ValueError, match="Project with ID 1 not found"):
        await project_service.delete_project(1)

    mock_repository.delete_project.assert_awaited_once_with(1)


@pytest.mark.asyncio
async def test_update_project(project_service, mock_repository, sample_project):
    mock_repository.update_project.return_value = sample_project

    updated_project = await project_service.update_project(1, sample_project)

    assert updated_project.id == sample_project.id
    assert updated_project.name == sample_project.name
    mock_repository.update_project.assert_awaited_once_with(1, sample_project)


@pytest.mark.asyncio
async def test_update_project_not_found(project_service, mock_repository, sample_project):
    mock_repository.update_project.return_value = None

    with pytest.raises(ValueError, match="Project with ID 1 not found"):
        await project_service.update_project(1, sample_project)

    mock_repository.update_project.assert_awaited_once_with(1, sample_project)
