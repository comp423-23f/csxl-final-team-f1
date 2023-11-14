"""Represent the status of the XL equipment space."""

from pydantic import BaseModel
from typing import Sequence

from .reservation import Reservation
from .availability import EquipmentAvailability
from .operating_hours import OperatingHours


class Status(BaseModel):
    """The status of the XL equipment space, including reservations, for a given user."""

    my_reservations: Sequence[Reservation]
    equipment_availability: Sequence[EquipmentAvailability]
    operating_hours: Sequence[OperatingHours]
