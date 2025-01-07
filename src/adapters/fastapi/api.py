from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from starlette.responses import JSONResponse

from src.adapters.fastapi.schemas import ProjectRequest, ProjectResponse
from src.core.entities.project import Project
from src.core.services.factory import get_project_service
from src.core.services.project_service import ProjectService

api_router = APIRouter(prefix="/v1")


@api_router.get("/projects/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int, service: ProjectService = Depends(get_project_service)
) -> ProjectResponse:
    try:
        project = await service.get_project_by_id(project_id)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    else:
        return ProjectResponse(
            id=project.id,
            name=project.name,
            description=project.description,
            start_date=project.start_date,
            end_date=project.end_date,
            area_of_interest=project.to_geojson(),
        )


@api_router.get("/projects/", response_model=list[ProjectResponse])
async def list_projects(service: ProjectService = Depends(get_project_service)) -> list[ProjectResponse]:
    projects = await service.list_projects()
    return [
        ProjectResponse(
            id=project.id,
            name=project.name,
            description=project.description,
            start_date=project.start_date.isoformat(),
            end_date=project.end_date.isoformat(),
            area_of_interest=project.to_geojson(),
        )
        for project in projects
    ]


@api_router.post("/projects/", response_model=ProjectResponse)
async def create_project(
    request: ProjectRequest, service: ProjectService = Depends(get_project_service)
) -> JSONResponse:
    project = await service.create_project(
        Project(
            name=request.name,
            description=request.description,
            start_date=request.start_date,
            end_date=request.end_date,
            area_of_interest=Project.from_geojson(request.area_of_interest),
        )
    )

    return JSONResponse({"status": "Success", "id": project.id})


@api_router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: int,
    service: ProjectService = Depends(get_project_service),
) -> None:
    try:
        await service.delete_project(project_id)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error,
        )
    else:
        return


@api_router.put("/projects/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    request: ProjectRequest,
    service: ProjectService = Depends(get_project_service),
) -> ProjectResponse:
    updated_project = await service.update_project(
        project_id,
        Project(
            name=request.name,
            description=request.description,
            start_date=request.start_date,
            end_date=request.end_date,
            area_of_interest=Project.from_geojson(request.area_of_interest),
        ),
    )

    if not updated_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {project_id} not found",
        )

    return ProjectResponse(
        id=updated_project.id,
        name=updated_project.name,
        description=updated_project.description,
        start_date=updated_project.start_date.isoformat(),
        end_date=updated_project.end_date.isoformat(),
        area_of_interest=updated_project.to_geojson(),
    )
