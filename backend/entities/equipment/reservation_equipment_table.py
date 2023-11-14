"""Join table between Reservation and Equipment entities."""

from sqlalchemy import Table, Column, ForeignKey
from ..entity_base import EntityBase

reservation_equipment_table = Table(
    "equipment__reservation_equipment",
    EntityBase.metadata,
    Column("reservation_id", ForeignKey("equipment__reservation.id"), primary_key=True),
    Column("equipment_id", ForeignKey("equipment__equipment.id"), primary_key=True),
)
