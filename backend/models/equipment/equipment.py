"""Equipment models a physical working space in the equipment space."""

from pydantic import BaseModel


class EquipmentIdentity(BaseModel):
    id: int


class Equipment(EquipmentIdentity, BaseModel):
    id: int
    name: str
    reservable: bool
    is_keyboard: bool
    is_mouse: bool
    is_vr: bool


class NewEquipment(Equipment, BaseModel):
    id: int | None = None
