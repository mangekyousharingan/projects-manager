import pytest
from datetime import date
from pydantic import ValidationError

from src.adapters.fastapi.schemas import ProjectRequest, ProjectResponse


@pytest.mark.parametrize(
    "valid_data",
    [
        {
            "id": 1,
            "name": "My Project",
            "description": "Test description",
            "start_date": date(2025, 1, 1),
            "end_date": date(2025, 12, 31),
            "area_of_interest": {
                "type": "MultiPolygon",
                "coordinates": [[[[30, 20], [45, 40], [10, 40], [30, 20]]]],
            },
        },
        {
            "id": 42,
            "name": "Survey X",
            "description": None,
            "start_date": date(2025, 2, 1),
            "end_date": date(2025, 3, 1),
            "area_of_interest": {
                "type": "MultiPolygon",
                "coordinates": [
                    [
                        [[-10, -10], [-10, 0], [0, 0], [0, -10], [-10, -10]]
                    ]
                ],
            },
        },
    ],
)
def test_project_response_valid(valid_data):
    project_resp = ProjectResponse(**valid_data)
    assert project_resp.id == valid_data["id"]
    assert project_resp.name == valid_data["name"]
    assert project_resp.start_date == valid_data["start_date"]
    assert project_resp.end_date == valid_data["end_date"]
    assert project_resp.area_of_interest["type"] == "MultiPolygon"


@pytest.mark.parametrize(
    "valid_data",
    [
        {
            "name": "New Development",
            "description": "Optional desc",
            "start_date": date(2025, 2, 1),
            "end_date": date(2025, 3, 1),
            "area_of_interest": {
                "type": "MultiPolygon",
                "coordinates": [
                    [
                        [[100, 0], [101, 0], [101, 1], [100, 1], [100, 0]]
                    ]
                ],
            },
        },
        {
            "name": "Short Survey",
            "description": None,
            "start_date": date(2025, 1, 1),
            "end_date": date(2025, 1, 2),
            "area_of_interest": {
                "type": "MultiPolygon",
                "coordinates": [[[[30, 20], [40, 20], [40, 30], [30, 20]]]],
            },
        },
    ],
)
def test_project_request_valid(valid_data):
    project_req = ProjectRequest(**valid_data)
    assert project_req.name == valid_data["name"]
    assert project_req.start_date == valid_data["start_date"]
    assert project_req.end_date == valid_data["end_date"]
    assert project_req.area_of_interest["type"] == "MultiPolygon"


@pytest.mark.parametrize(
    "name, description, start_date, end_date, area_of_interest, expected_error",
    [
        (
            "Invalid Dates",
            "End date is before or same as start date",
            date(2025, 5, 1),
            date(2025, 5, 1),
            {
                "type": "MultiPolygon",
                "coordinates": [[[[30, 20], [45, 40], [10, 40], [30, 20]]]],
            },
            "end_date must be after start_date",
        ),
        (
            "Missing Dates",
            None,
            None,
            None,
            {
                "type": "MultiPolygon",
                "coordinates": [[[[30, 20], [45, 40], [10, 40], [30, 20]]]],
            },
            "Field required",
        ),
        # 3) Invalid geometry type
        (
            "Wrong GeoJSON",
            "Not a MultiPolygon",
            date(2025, 1, 1),
            date(2025, 2, 1),
            {
                "type": "Polygon",  # not MultiPolygon
                "coordinates": [[[[30, 20], [45, 40], [10, 40], [30, 20]]]],
            },
            "area_of_interest must have a type of 'MultiPolygon'",
        ),
        (
            "Bad GeoJSON",
            None,
            date(2025, 3, 1),
            date(2025, 4, 1),
            {
                "type": "MultiPolygon",
                "coordinatesss": [[[[30, 20], [45, 40], [10, 40], [30, 20]]]],
            },
            "Invalid GeoJSON format for area_of_interest",
        ),
        (
            "X" * 33,
            None,
            date(2025, 1, 1),
            date(2025, 1, 2),
            {
                "type": "MultiPolygon",
                "coordinates": [[[[30, 20], [45, 40], [10, 40], [30, 20]]]],
            },
            "String should have at most 32 characters",
        ),
    ],
)
def test_project_request_invalid(
    name,
    description,
    start_date,
    end_date,
    area_of_interest,
    expected_error,
):
    input_data = {"name": name}
    if description is not None:
        input_data["description"] = description
    if start_date is not None:
        input_data["start_date"] = start_date
    if end_date is not None:
        input_data["end_date"] = end_date
    if area_of_interest is not None:
        input_data["area_of_interest"] = area_of_interest

    with pytest.raises(ValidationError) as exc_info:
        ProjectRequest(**input_data)

    error_str = str(exc_info.value)
    assert expected_error in error_str, (
        f"Expected error '{expected_error}' not found. Actual errors: {error_str}"
    )
