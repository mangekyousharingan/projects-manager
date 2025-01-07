from unittest.mock import MagicMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.database.factory import get_project_repository
from src.adapters.database.repository import ProjectRepository
from src.core.ports.project_repository import ProjectRepositoryPort


@pytest.mark.asyncio
async def test_get_project_repository_factory():
    mock_session = MagicMock(spec=AsyncSession)

    repo = get_project_repository(mock_session)

    assert isinstance(repo, ProjectRepository)
    assert isinstance(repo, ProjectRepositoryPort)
    assert repo.session is mock_session
