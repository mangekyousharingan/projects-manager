from datetime import date
import json
from typing import Any

from geoalchemy2 import WKBElement
from shapely import from_geojson, to_geojson
from shapely.wkb import loads as wkb_loads


class Project:
    def __init__(
        self,
        name: str,
        description: str | None,
        start_date: date,
        end_date: date,
        area_of_interest: WKBElement,
        id: int | None = None,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.area_of_interest = area_of_interest

    def to_geojson(self) -> dict | Any:
        """Convert Geometry to GeoJSON for API responses."""
        if self.area_of_interest:
            shapely_geometry = wkb_loads(bytes(self.area_of_interest.data))
            area_of_interest = to_geojson(shapely_geometry)
            return json.loads(area_of_interest)
        return {}

    @staticmethod
    def from_geojson(geojson: dict[str, Any]) -> WKBElement:
        """Convert GeoJSON to WKTElement for database storage."""
        geojson_str = json.dumps(geojson)
        shapely_geometry = from_geojson(geojson_str)
        sqlalchemy_geometry = WKBElement(shapely_geometry.wkb, srid=4326)
        return sqlalchemy_geometry
