"""
The Equipment Service allows the API to manipulate organizations data in the database.
"""

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import db_session
from ..models.equipment import Equipment
from ..models.equipment.equipment_details import EquipmentDetails
from ..entities.equipment.equipment_entity import EquipmentEntity
from ..models import User
from .permission import PermissionService

from .exceptions import EquipmentNotFoundException
from .exceptions import UserPermissionException


class EquipmentService:
    """Service that performs all of the actions on the `Equipment` table"""

    def __init__(
        self,
        session: Session = Depends(db_session),
        permission: PermissionService = Depends(),
    ):
        """Initializes the `EquipmentService` session, and `PermissionService`"""
        self._session = session
        self._permission = permission

    def all(self) -> list[Equipment]:
        """
        Retrieves all equipment from the table

        Returns:
            list[Equipment]: List of all `Equipment`
        """
        # Select all entries in `Organization` table
        query = select(EquipmentEntity)
        entities = self._session.scalars(query).all()

        # Convert entries to a model and return
        return [entity.to_model() for entity in entities]
