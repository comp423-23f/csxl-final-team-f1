"""Tests for Coworking Operating Hours Service."""

from ....services.equipment.operating_hours import OperatingHoursService
from ....models.equipment import TimeRange
from ....models.equipment.operating_hours import OperatingHours

# Imported fixtures provide dependencies injected for the tests as parameters.
from .fixtures import operating_hours_svc
from .equipment_time import *

# Insert fake data entities in database
from .equipment_operating_hours_data import fake_data_fixture

# Import the fake model data in a namespace for test assertions
from . import equipment_operating_hours_data


def test_schedule_closed(
    operating_hours_svc: OperatingHoursService, time: dict[str, datetime]
):
    """When there are no operating hours open in a given time range, returns an empty list."""
    time_range = TimeRange(start=time[A_WEEK_AGO], end=time[A_WEEK_AGO] + ONE_HOUR)
    result: list[OperatingHours] = operating_hours_svc.schedule(time_range)
    assert len(result) == 0


def test_schedule_one_match(
    operating_hours_svc: OperatingHoursService, time: dict[str, datetime]
):
    """When one OperatingHours matches the time range, returns a list with just it."""
    time_range = TimeRange(start=time[NOW], end=time[IN_ONE_HOUR])
    result: list[OperatingHours] = operating_hours_svc.schedule(time_range)
    assert len(result) == 1
    assert result[0].id == equipment_operating_hours_data.today.id


def test_schedule_multiple_match(
    operating_hours_svc: OperatingHoursService, time: dict[str, datetime]
):
    """When one OperatingHours matches the time range, returns a list with just it."""
    time_range = TimeRange(start=time[TOMORROW], end=time[TOMORROW] + ONE_DAY)
    result: list[OperatingHours] = operating_hours_svc.schedule(time_range)
    assert len(result) == 2
    assert result[0].id == equipment_operating_hours_data.tomorrow.id
    assert result[1].id == equipment_operating_hours_data.future.id
