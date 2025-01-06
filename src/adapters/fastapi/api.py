from fastapi import APIRouter

from src.adapters.fastapi.schemas import ProjectCreateRequest, ProjectResponse

api_router = APIRouter()


@api_router.get("/projects/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: int) -> None:
    pass


@api_router.get("/projects/", response_model=ProjectResponse)
async def create_project(request: ProjectCreateRequest) -> None:
    print(request.model_dump())
