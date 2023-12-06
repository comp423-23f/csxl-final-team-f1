"""Join table between Reservation and Seat entities."""

from sqlalchemy import Table, Column, ForeignKey
from ..entity_base import EntityBase


equipment_reservation_user_table = Table(
    "equipment__reservation_user",
    EntityBase.metadata,
    Column("reservation_id", ForeignKey("equipment__reservation.id"), primary_key=True),
    Column("user_id", ForeignKey("user.id"), primary_key=True),
)
