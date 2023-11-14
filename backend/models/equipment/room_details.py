"""RoomDetails provides more information about a room in the equipment space.

Importantly, it includes a room's equipment, if equipments are reservable as in the XL collab.
"""

from .room import Room
from .equipment import Equipment


class RoomDetails(Room):
    building: str
    room: str
    capacity: int
    reservable: bool
    equipment: list[Equipment] = []

    def to_room(self) -> Room:
        """Converts the details model to a room model.

        Returns:
            Room: The model representation of the entity."""
        return Room(id=self.id, nickname=self.nickname)
