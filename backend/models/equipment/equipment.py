"""Equipment models a piece of reservable equipment."""

from pydantic import BaseModel


class EquipmentIdentity(BaseModel):
    id: int


class Equipment(EquipmentIdentity, BaseModel):
    id: int
    name: str
    reservable: bool
    image: str


class NewEquipment(Equipment, BaseModel):
    id: int | None = None
