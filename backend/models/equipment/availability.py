"""Models for the availability of equipment over a time range."""

from pydantic import BaseModel, validator

from .equipment import Equipment
from .time_range import TimeRange
from .availability_list import AvailabilityList


class EquipmentAvailability(Equipment, AvailabilityList, BaseModel):
    """A equipment that is available for a given time range."""

    ...
