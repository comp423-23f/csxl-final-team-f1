"""Entity for Room."""

from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..entity_base import EntityBase
from ...models.equipment import Room, RoomDetails
from typing import Self


class RoomEntity(EntityBase):
    """Entity for Rooms under XL management."""

    __tablename__ = "equipment__room"

    # Room Model Fields
    id: Mapped[str] = mapped_column(String, primary_key=True)
    capacity: Mapped[int] = mapped_column(Integer, index=True)
    # RoomDetails Model Fields Follow
    building: Mapped[str] = mapped_column(String)
    room: Mapped[str] = mapped_column(String)
    nickname: Mapped[str] = mapped_column(String)
    reservable: Mapped[bool] = mapped_column(Boolean)

    equipment: Mapped[list["EquipmentEntity"]] = relationship(  # type: ignore
        "EquipmentEntity", back_populates="room"
    )

    def to_model(self) -> Room:
        """Converts the entity to a model.

        Returns:
            Room: The model representation of the entity."""
        return Room(id=self.id, nickname=self.nickname)

    def to_details_model(self) -> RoomDetails:
        """Converts the entity to a RoomDetail model.

        Returns:
            RoomDetails: The model representation of the entity."""
        return RoomDetails(
            id=self.id,
            nickname=self.nickname,
            building=self.building,
            room=self.room,
            capacity=self.capacity,
            reservable=self.reservable,
            equipment=[equipment.to_model() for equipment in self.equipment],
        )

    @classmethod
    def from_model(cls, model: RoomDetails) -> Self:
        """Create an RoomEntity from a Room model.

        Args:
            model (Room): The model to create the entity from.

        Returns:
            Self: The entity (not yet persisted)."""
        return cls(
            id=model.id,
            nickname=model.nickname,
            building=model.building,
            room=model.room,
            capacity=model.capacity,
            reservable=model.reservable,
        )
