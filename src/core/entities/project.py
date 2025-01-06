from datetime import date

from geoalchemy2 import Geometry
from pydantic import BaseModel


class Project(BaseModel):
    id: int | None
    name: str
    description: str | None
    start_date: date
    end_date: date
    area_of_interest: Geometry
