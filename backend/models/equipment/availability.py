"""Models for the availability of rooms and seats over a time range."""

from pydantic import BaseModel, validator

from .equipment import Equipment
from .time_range import TimeRange
from .availability_list import AvailabilityList


class EquipmentAvailability(Equipment, AvailabilityList):
    """A equipment that is available for a given time range."""

    ...
