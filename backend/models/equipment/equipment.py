"""Seat models a physical working space in the coworking space."""

from pydantic import BaseModel


class EquipmentIdentity(BaseModel):
    id: int


class Equipment(EquipmentIdentity, BaseModel):
    id: int
    name: str
    reservable: bool


class NewEquipment(Equipment, BaseModel):
    id: int | None = None
