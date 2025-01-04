from geoalchemy2 import Geometry
from sqlalchemy import Date, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.adapters.database.tables.base import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    start_date: Mapped[Date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Date] = mapped_column(Date, nullable=False)
    area_of_interest: Mapped[str] = mapped_column(Geometry("MULTIPOLYGON"), nullable=False)
