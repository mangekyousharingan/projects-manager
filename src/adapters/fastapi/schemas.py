from datetime import date
import json
from typing import Any

import geojson
from pydantic import BaseModel, Field, ValidationInfo, field_validator


class ProjectResponse(BaseModel):
    id: int = Field(
        ...,
        title="Project ID",
        description="Unique identifier for the project.",
        json_schema_extra={
            "type": "integer",
            "example": 1,
        },
    )
    name: str = Field(
        ...,
        title="Project Name",
        description="Name of the project (maximum 32 characters).",
        max_length=32,
        json_schema_extra={
            "type": "string",
            "example": "Land Survey Project",
        },
    )
    description: str | None = Field(
        None,
        title="Description",
        description="Detailed description of the project.",
        json_schema_extra={
            "type": "string",
            "example": "Analyzing a plot of land for development.",
        },
    )
    start_date: date = Field(
        ...,
        title="Start Date",
        description="The start date of the project (ISO 8601 format).",
        json_schema_extra={
            "type": "string",
            "format": "date",
            "example": "2025-01-01",
        },
    )
    end_date: date = Field(
        ...,
        title="End Date",
        description="The end date of the project (ISO 8601 format).",
        json_schema_extra={
            "type": "string",
            "format": "date",
            "example": "2025-12-31",
        },
    )
    area_of_interest: dict[str, Any] = Field(
        ...,
        title="GeoJSON Data",
        description="A valid GeoJSON object of type 'MultiPolygon'.",
        json_schema_extra={
            "type": "object",
            "title": "GeoJSON MultiPolygon",
            "description": "GeoJSON object with type 'MultiPolygon' and valid coordinates.",
            "example": {
                "type": "MultiPolygon",
                "coordinates": [[[[30, 20], [45, 40], [10, 40], [30, 20]]]],
            },
        },
    )


class ProjectRequest(BaseModel):
    name: str = Field(
        ...,
        max_length=32,
        title="Project Name",
        description="Name of the project (maximum 32 characters).",
        json_schema_extra={
            "type": "string",
            "example": "New Development Project",
        },
    )
    description: str | None = Field(
        None,
        title="Description",
        description="Optional description of the project.",
        json_schema_extra={
            "type": "string",
            "example": "A detailed survey of the land.",
        },
    )
    start_date: date = Field(
        ...,
        title="Start Date",
        description="The starting date of the project (ISO 8601 format).",
        json_schema_extra={
            "type": "string",
            "format": "date",
            "example": "2025-02-01",
        },
    )
    end_date: date = Field(
        ...,
        title="End Date",
        description="The ending date of the project (ISO 8601 format).",
        json_schema_extra={
            "type": "string",
            "format": "date",
            "example": "2025-11-30",
        },
    )
    area_of_interest: dict[str, Any] = Field(
        ...,
        title="GeoJSON Area",
        description="A GeoJSON object describing the project's area of interest.",
        json_schema_extra={
            "type": "object",
            "title": "GeoJSON MultiPolygon",
            "description": "GeoJSON object with type 'MultiPolygon' and valid coordinates.",
            "example": {
                "type": "MultiPolygon",
                "coordinates": [[[[30, 20], [45, 40], [10, 40], [30, 20]]]],
            },
        },
    )

    @field_validator("area_of_interest")
    @classmethod
    def validate_geojson(cls, area_of_interest: dict[str, Any]) -> dict[str, Any]:
        try:
            geojson_obj = geojson.loads(json.dumps(area_of_interest))
            if geojson_obj["type"] != "MultiPolygon":
                raise ValueError("area_of_interest must have a type of 'MultiPolygon'.")
        except Exception as exc:
            raise ValueError(f"Invalid GeoJSON format for area_of_interest: {exc}")
        return area_of_interest

    @field_validator("end_date", mode="after")
    @classmethod
    def validate_dates(cls, end_date: date, info: ValidationInfo) -> date:
        start_date = info.data.get("start_date")
        if start_date and end_date <= start_date:
            raise ValueError("end_date must be after start_date.")
        return end_date
