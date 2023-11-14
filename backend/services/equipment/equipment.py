"""Service that manages equipments in the equipment space."""

from fastapi import Depends
from sqlalchemy.orm import Session
from ...database import db_session
from ...models.equipment import Equipment, EquipmentDetails
from ...entities.equipment import EquipmentEntity


class EquipmentService:
    """EquipmentService is the access layer to equipment equipment."""

    def __init__(self, session: Session = Depends(db_session)):
        """Initializes a new RoomService.

        Args:
            session (Session): The database session to use, typically injected by FastAPI.
        """
        self._session = session

    def list(self) -> list[EquipmentDetails]:
        """Returns all equipments in the equipment space.

        Returns:
            list[EquipmentDetails]: All rooms in the equipment space orderd by increasing capacity.
        """
        entities = self._session.query(EquipmentEntity).all()
        return [entity.to_model() for entity in entities]
