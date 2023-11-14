from enum import Enum
from pydantic import BaseModel
from datetime import datetime
from ...models.user import User, UserIdentity
from .room import Room
from .equipment import Equipment, EquipmentIdentity
from .time_range import TimeRange


class ReservationState(str, Enum):
    DRAFT = "DRAFT"
    CONFIRMED = "CONFIRMED"
    CHECKED_IN = "CHECKED_IN"
    CHECKED_OUT = "CHECKED_OUT"
    CANCELLED = "CANCELLED"


class ReservationIdentity(BaseModel):
    id: int


class ReservationRequest(TimeRange):
    users: list[UserIdentity] = []
    equipment: list[EquipmentIdentity] = []


class Reservation(ReservationIdentity, TimeRange):
    state: ReservationState
    users: list[User] = []
    equipment: list[Equipment] = []
    room: Room | None = None
    walkin: bool = False
    created_at: datetime
    updated_at: datetime


class ReservationPartial(Reservation, BaseModel):
    start: datetime | None = None
    end: datetime | None = None
    state: ReservationState | None = None
    users: list[User] | None = None
    equipment: list[Equipment] | None = None
    room: Room | None = None
    walkin: bool | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class ReservationDetails(Reservation):
    errors: list[str] = []
    extendable: bool = False
    extendable_at: datetime | None
    extendable_until: datetime | None
