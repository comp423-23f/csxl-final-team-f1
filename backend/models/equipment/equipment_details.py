"""EquipmentDetails extends information about an equipment, including its Room, to the equipment model."""

from pydantic import BaseModel

from .equipment import Equipment
from .room import Room


class EquipmentDetails(Equipment, BaseModel):
    room: Room
