"""Definition of SQLAlchemy table-backed object mapping entity for Organizations."""

from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session, joinedload
from ..entity_base import EntityBase
from ...models.equipment import EquipmentDetails
from ...models.equipment.equipment import EquipmentIdentity, Equipment
from typing import Self


class EquipmentEntity(EntityBase):
    """Entity for Seats under XL management."""

    __tablename__ = "equipment"

    # Unique ID for the equipment
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # Name of the equipment
    name: Mapped[str] = mapped_column(String, nullable=False, default="")
    # Image of the equipment
    image: Mapped[str] = mapped_column(String)
    # Short description of the equipment
    description: Mapped[str] = mapped_column(String)
    # Whether the equipment can be reserved by anyone or not
    reservable: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    # x: Mapped[int] = mapped_column(Integer)
    # y: Mapped[int] = mapped_column(Integer)
    # # EquipmentDetails Model Fields Follow
    # room_id: Mapped[str] = mapped_column(String, ForeignKey("coworking__room.id"))

    room: Mapped["RoomEntity"] = relationship("RoomEntity", back_populates="seats")  # type: ignore

    def to_model(self) -> EquipmentDetails:
        """Converts the entity to a model.

        Returns:
            Seat: The model representation of the entity."""
        return EquipmentDetails(
            id=self.id,
            name=self.name,
            image=self.image,
            reservable=self.reservable,
            description=self.description,
            # x=self.x,
            # y=self.y,
            room=self.room.to_model(),
        )

    @classmethod
    def get_models_from_identities(
        cls, session: Session, identities: list[EquipmentIdentity]
    ) -> list[Equipment]:
        equipment_ids = [equipment.id for equipment in identities]
        entities = session.query(cls).filter(cls.id.in_(equipment_ids)).all()
        return [entity.to_model() for entity in entities]

    @classmethod
    def from_model(cls, model: EquipmentDetails) -> Self:
        """Create an SeEntity from a Seat model.

        Args:
            model (Seat): The model to create the entity from.

        Returns:
            Self: The entity (not yet persisted)."""
        return cls(
            id=model.id,
            name=model.name,
            description=model.description,
            reservable=model.reservable,
            image=model.image,
        )
