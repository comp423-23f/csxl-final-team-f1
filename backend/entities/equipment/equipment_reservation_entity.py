"""Entity for Reservations."""

from datetime import datetime
from sqlalchemy import Integer, String, Boolean, ForeignKey, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from ..entity_base import EntityBase
from ...models.equipment import Reservation, ReservationState
from .equipment_entity import EquipmentEntity
from ..user_entity import UserEntity
from .reservation_user_table import equipment_reservation_user_table
from .reservation_equipment_table import equipment_reservation_equipment_table
from typing import Self


class ReservationEntity(EntityBase):
    __tablename__ = "equipment__reservation"
    __table_args__ = (
        Index("reservation_time_idx", "start", "end", "state", unique=False),
    )

    # Reservation Model Fields
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    state: Mapped[ReservationState] = mapped_column(String, nullable=False)
    walkin: Mapped[bool] = mapped_column(Boolean, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )
    # user_pid: Mapped[int] = mapped_column(ForeignKey("user.pid"))
    # equipment_id: Mapped[int] = mapped_column(ForeignKey("equipment.id"))

    # equipment: Mapped["EquipmentEntity"] = relationship(back_populates="registrations")
    # user: Mapped["UserEntity"] = relationship(back_populates="registrations")

    # Relationships
    users: Mapped[list[UserEntity]] = relationship(
        secondary=equipment_reservation_user_table
    )
    equipment: Mapped[list[EquipmentEntity]] = relationship(
        secondary=equipment_reservation_equipment_table
    )

    def to_model(self) -> Reservation:
        """Converts the entity to a model.

        Returns:
            Reservation: The model representation of the entity."""
        return Reservation(
            id=self.id,
            start=self.start,
            end=self.end,
            state=self.state,
            walkin=self.walkin,
            created_at=self.created_at,
            updated_at=self.updated_at,
            users=[user.to_model() for user in self.users],
            equipment=[x.to_model() for x in self.equipment],
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
            walkin=model.walkin,
            users=[session.get(UserEntity, user.id) for user in model.users]
            if session
            else [],
            equipment=[session.get(EquipmentEntity, x.id) for x in model.equipment]
            if session
            else [],
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
