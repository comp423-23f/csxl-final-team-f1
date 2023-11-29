"""Entity for Equipment."""

from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session, joinedload
from ..entity_base import EntityBase
from ...models.equipment.equipment import EquipmentIdentity, Equipment
from typing import Self


class EquipmentEntity(EntityBase):
    """Entity for Equipment under XL management."""

    __tablename__ = "equipment__equipment"

    # Equipment Model Fields
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    reservable: Mapped[bool] = mapped_column(Boolean)

    # registrations: Mapped[list["EquipmentReservationEntity"]] = relationship(
    #     back_populates="equipment", cascade="all,delete"
    # )

    def to_model(self) -> Equipment:
        """Converts the entity to a model.

        Returns:
            equipment: The model representation of the entity."""
        return Equipment(
            id=self.id,
            name=self.name,
            reservable=self.reservable,
        )

    @classmethod
    def get_models_from_identities(
        cls, session: Session, identities: list[EquipmentIdentity]
    ) -> list[Equipment]:
        equipment_ids = [x.id for x in identities]
        entities = (
            session.query(cls).filter(cls.id.in_(equipment_ids))
            # .options(joinedload(EquipmentEntity.room))
            .all()
        )
        return [entity.to_model() for entity in entities]

    @classmethod
    def from_model(cls, model: Equipment) -> Self:
        """Create an EquipmentEntity from a Equipment model.

        Args:
            model (Equipment): The model to create the entity from.

        Returns:
            Self: The entity (not yet persisted)."""
        return cls(
            id=model.id,
            name=model.name,
            reservable=model.reservable,
        )
