"""EquipmentDetails extends information about Equipment, including its Room, to the Seat model."""

from pydantic import BaseModel

from .equipment import Equipment
from ..coworking import Room

class EquipmentDetails(Equipment, BaseModel):
    room: Room
