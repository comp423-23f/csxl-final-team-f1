"""Entity for Equipment."""

from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session, joinedload
from ..entity_base import EntityBase
from ...models.equipment import EquipmentDetails
from ...models.equipment.equipment import EquipmentIdentity, Equipment
from typing import Self


class EquipmentEntity(EntityBase):
    """Entity for Equipment under XL management."""

    __tablename__ = "equipment"

    # Equipment Model Fields
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    reservable: Mapped[bool] = mapped_column(Boolean)
    # EquipmentDetails Model Fields Follow
    room_id: Mapped[str] = mapped_column(String, ForeignKey("room.id"))

    room: Mapped["RoomEntity"] = relationship("RoomEntity", back_populates="equipment")  # type: ignore

    def to_model(self) -> EquipmentDetails:
        """Converts the entity to a model.

        Returns:
            equipment: The model representation of the entity."""
        return EquipmentDetails(
            id=self.id,
            name=self.name,
            reservable=self.reservable,
            room=self.room.to_model(),
        )

    @classmethod
    def get_models_from_identities(
        cls, session: Session, identities: list[EquipmentIdentity]
    ) -> list[Equipment]:
        equipment_ids = [equipment.id for equipment in identities]
        entities = (
            session.query(cls)
            .filter(cls.id.in_(equipment_ids))
            .options(joinedload(EquipmentEntity.room))
            .all()
        )
        return [entity.to_model() for entity in entities]

    @classmethod
    def from_model(cls, model: EquipmentDetails) -> Self:
        """Create an EquipmentEntity from a Equipment model.

        Args:
            model (Equipment): The model to create the entity from.

        Returns:
            Self: The entity (not yet persisted)."""
        return cls(
            id=model.id,
            name=model.name,
            reservable=model.reservable,
            room_id=model.room.id,
        )
