from datetime import date
import json
from unittest.mock import Mock

from geoalchemy2 import WKBElement
from shapely import to_geojson
from shapely.geometry import Polygon
from shapely.wkb import dumps as wkb_dumps

from src.core.entities.project import Project


def create_mock_wkbelement(geometry):
    wkb_data = wkb_dumps(geometry)
    mock_wkb = Mock(spec=WKBElement)
    mock_wkb.data = wkb_data
    return mock_wkb


def test_project_initialization():
    mock_geometry = create_mock_wkbelement(Polygon([(0, 0), (1, 0), (1, 1), (0, 0)]))
    project = Project(
        name="Test Project",
        description="A test description",
        start_date=date(2025, 1, 1),
        end_date=date(2025, 12, 31),
        area_of_interest=mock_geometry,
        id=1,
    )

    assert project.id == 1
    assert project.name == "Test Project"
    assert project.description == "A test description"
    assert project.start_date == date(2025, 1, 1)
    assert project.end_date == date(2025, 12, 31)
    assert project.area_of_interest == mock_geometry


def test_to_geojson():
    polygon = Polygon([(0, 0), (1, 0), (1, 1), (0, 0)])
    mock_geometry = create_mock_wkbelement(polygon)
    project = Project(
        name="Test Project",
        description="A test description",
        start_date=date(2025, 1, 1),
        end_date=date(2025, 12, 31),
        area_of_interest=mock_geometry,
    )

    geojson = project.to_geojson()
    expected_geojson = json.loads(to_geojson(polygon))

    assert geojson == expected_geojson


def test_to_geojson_no_geometry():
    project = Project(
        name="Test Project",
        description="A test description",
        start_date=date(2025, 1, 1),
        end_date=date(2025, 12, 31),
        area_of_interest=None,
    )

    geojson = project.to_geojson()
    assert geojson == {}


def test_from_geojson():
    geojson = {
        "type": "Polygon",
        "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 0]]],
    }

    wkb_element = Project.from_geojson(geojson)

    shapely_geometry = Polygon([(0, 0), (1, 0), (1, 1), (0, 0)])
    expected_wkb = wkb_dumps(shapely_geometry)

    assert isinstance(wkb_element, WKBElement)
    assert wkb_element.data == expected_wkb
    assert wkb_element.srid == 4326
