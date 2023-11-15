"""Entity for Reservations."""

from datetime import datetime
from sqlalchemy import Integer, String, Boolean, ForeignKey, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from ..entity_base import EntityBase
from ...models.equipment import Reservation, ReservationState
from .equipment_entity import EquipmentEntity
from ..user_entity import UserEntity

# from .reservation_user_table import reservation_user_table
# from .reservation_equipment_table import reservation_equipment_table
from typing import Self


class ReservationEntity(EntityBase):
    __tablename__ = "equipment_reservation"
    __table_args__ = (
        Index("reservation_time_idx", "start", "end", "state", unique=False),
    )

    # Reservation Model Fields
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    equipment_id: Mapped[int] = mapped_column(ForeignKey("equipment_id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user_id"))
    start: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    state: Mapped[ReservationState] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )

    # Relationships
    user: Mapped[UserEntity] = relationship("UserEntity")
    equipment: Mapped[list[EquipmentEntity]] = relationship("EquipmentEntity")

    def to_model(self) -> Reservation:
        """Converts the entity to a model.

        Returns:
            Reservation: The model representation of the entity."""
        return Reservation(
            id=self.id,
            start=self.start,
            end=self.end,
            state=self.state,
            user=self.user.to_model(),
            equipment=[equipment.to_model() for equipment in self.equipment],
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @classmethod
    def from_model(cls, model: Reservation, session: Session | None = None) -> Self:
        """Create an ReservationEntity from a Reservation model.

        Args:
            model (Reservation): The model to create the entity from.

        Returns:
            Self: The entity (not yet persisted)."""

        return cls(
            id=model.id,
            start=model.start,
            end=model.end,
            state=model.state,
            user=session.get(UserEntity, id) if session else [],
            equipment=[
                session.get(EquipmentEntity, equipment.id)
                for equipment in model.equipment
            ]
            if session
            else [],
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
