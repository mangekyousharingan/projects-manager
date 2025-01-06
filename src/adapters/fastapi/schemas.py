import json

import geojson
from pydantic import BaseModel, Field, field_validator
from datetime import date
from typing import Any


class ProjectCreateRequest(BaseModel):
    name: str = Field(..., max_length=32)
    description: str | None
    start_date: date
    end_date: date
    area_of_interest: dict[str, Any]

    @field_validator("area_of_interest")
    def validate_geojson(self, area_of_interest: dict[str, Any]) -> dict[str, Any]:
        try:
            geojson_obj = geojson.loads(json.dumps(area_of_interest))
            if geojson_obj["type"] != "MultiPolygon":
                raise ValueError("area_of_interest must have a type of 'MultiPolygon'.")
        except Exception as exc:
            raise ValueError(f"Invalid GeoJSON format for area_of_interest: {exc}")
        return area_of_interest

    @field_validator("end_date", mode="before")
    def validate_dates(self, end_date: date, values: dict[str, Any]) -> date:
        start_date = values.get("start_date")
        if start_date and end_date <= start_date:
            raise ValueError("end_date must be after start_date.")
        return end_date


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str | None
    start_date: str
    end_date: str
    area_of_interest: dict[str, Any] = Field(
        ...,
        title="GeoJSON Data",
        description="A valid GeoJSON object of type 'MultiPolygon'.",
        json_schema_extra={
            "type": "MultiPolygon",
            "coordinates": [
                [
                    [[30, 20], [45, 40], [10, 40], [30, 20]]
                ]
            ]
        },
    )
