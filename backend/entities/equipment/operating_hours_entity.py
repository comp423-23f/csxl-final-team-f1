"""Entity for Operating Hours.""" ""

from sqlalchemy import Integer, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..entity_base import EntityBase
from ...models.equipment.operating_hours import OperatingHours
from datetime import datetime
from typing import Self


class OperatingHoursEntity(EntityBase):
    """Entity for Operating Hours."""

    __tablename__ = "equipment__operating_hours"
    __table_args__ = (
        Index("equipment__operating_hours_idx", "start", "end", unique=False),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start: Mapped[datetime] = mapped_column(DateTime, index=True)
    end: Mapped[datetime] = mapped_column(DateTime, index=True)

    def to_model(self) -> OperatingHours:
        """Converts the entity to a model.

        Returns:
            OperatingHours: The model representation of the entity."""
        return OperatingHours(id=self.id, start=self.start, end=self.end)

    @classmethod
    def from_model(cls, model: OperatingHours) -> Self:
        """Create an OperatingHoursEntity from a OperatingHours model.

        Args:
            model (OperatingHours): The model to create the entity from.

        Returns:
            Self: The entity (not yet persisted)."""
        return cls(id=model.id, start=model.start, end=model.end)
