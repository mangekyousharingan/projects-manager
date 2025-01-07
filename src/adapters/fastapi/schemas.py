from datetime import date
import json
from typing import Any

import geojson
from pydantic import BaseModel, Field, field_validator
from pydantic_core.core_schema import ValidationInfo


class ProjectRequest(BaseModel):
    name: str = Field(..., max_length=32)
    description: str | None
    start_date: date
    end_date: date
    area_of_interest: dict[str, Any]

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


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str | None
    start_date: date
    end_date: date
    area_of_interest: dict[str, Any] = Field(
        ...,
        title="GeoJSON Data",
        description="A valid GeoJSON object of type 'MultiPolygon'.",
        json_schema_extra={
            "type": "MultiPolygon",
            "coordinates": [[[[30, 20], [45, 40], [10, 40], [30, 20]]]],
        },
    )
