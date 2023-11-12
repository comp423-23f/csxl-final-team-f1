"""Definition of SQLAlchemy table-backed object mapping entity for Equipment."""

from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..entity_base import EntityBase
from typing import Self
from ...models.equipment.equipment import Equipment


class EquipmentEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `Equipment` table"""

    # Name for the equipment table in the PostgreSQL database
    __tablename__ = "equipment"

    # Equipment properties (columns in the database table)

    # Unique ID for the device
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # Name of the device
    name: Mapped[str] = mapped_column(String, nullable=False, default="")

    @classmethod
    def from_model(cls, model: Equipment) -> Self:
        """
        Class method that converts an `Equipment` model into a `EquipmentEntity`

        Parameters:
            - model (Equipment): Model to convert into an entity
        Returns:
            EquipmentEntity: Entity created from model
        """
        return cls(
            id=model.id,
            name=model.name,
        )

    def to_model(self) -> Equipment:
        """
        Converts a `EquipmentEntity` object into a `Equipment` model object

        Returns:
            Equipment: `Equipment` object from the entity
        """
        return Equipment(
            id=self.id,
            name=self.name,
        )
