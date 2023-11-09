"""
The Equipment Service allows the API to manipulate organizations data in the database.
"""

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import db_session
from ..models.equipment import Equipment
from ..entities.equipment_entity import EquipmentEntity
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

    def create(self, subject: User, equipment: Equipment) -> Equipment:
        """
        Creates a organization based on the input object and adds it to the table.
        If the organization's ID is unique to the table, a new entry is added.
        If the organization's ID already exists in the table, it raises an error.

        Parameters:
            subject: a valid User model representing the currently logged in User
            organization (Organization): Organization to add to table

        Returns:
            Organization: Object added to table
        """

        # Check if user has admin permissions
        self._permission.enforce(subject, "organization.create", f"organization")

        # Checks if the organization already exists in the table
        if equipment.id:
            # Set id to None so database can handle setting the id
            equipment.id = None

        else:
            # Otherwise, create new object
            equipment_entity = EquipmentEntity.from_model(equipment)

            # Add new object to table and commit changes
            self._session.add(equipment_entity)
            self._session.commit()

            # Return added object
            return equipment_entity.to_model()

    def get_from_id(self, id: int) -> Equipment:
        """
        Get the organization from a slug
        If none retrieved, a debug description is displayed.

        Parameters:
            slug: a string representing a unique organization slug

        Returns:
            Organization: Object with corresponding slug

        Raises:
            OrganizationNotFoundException if no organization is found with the corresponding slug
        """

        # Query the organization with matching slug
        equipment = (
            self._session.query(EquipmentEntity)
            .filter(EquipmentEntity.id == id)
            .one_or_none()
        )

        # Check if result is null
        if equipment:
            # Convert entry to a model and return
            return equipment.to_model()
        else:
            # Raise exception
            raise EquipmentNotFoundException(id)

    def update(self, subject: User, equipment: Equipment) -> Equipment:
        """
        Update the equipment
        If none found with that id, a debug description is displayed.

        Parameters:
            subject: a valid User model representing the currently logged in User
            equipment (Equipment): Equipment to add to table

        Returns:
            Equipment: Updated equipment object

        Raises:
            EquipmentNotFoundException: If no equipment is found with the corresponding id
        """

        # Check if user has admin permissions
        self._permission.enforce(subject, "equipment.create", f"equipment")

        # Query the equipment with matching id
        obj = self._session.get(EquipmentEntity, equipment.id)

        # Check if result is null
        if obj:
            # Update equipment object
            obj.name = equipment.name

            # Save changes
            self._session.commit()

            # Return updated object
            return obj.to_model()
        else:
            # Raise exception
            raise EquipmentNotFoundException(equipment.id)

    def delete(self, subject: User, id: int) -> None:
        """
        Delete the equipment based on the provided id.
        If no item exists to delete, a debug description is displayed.

        Parameters:
            subject: a valid User model representing the currently logged in User
            id: an integer representing a unique equipment id

        Raises:
            EquipmentNotFoundException: If no equipment is found with the corresponding id
        """
        # Check if user has admin permissions
        self._permission.enforce(subject, "equipment.create", f"equipment")

        # Find object to delete
        obj = (
            self._session.query(EquipmentEntity)
            .filter(EquipmentEntity.id == id)
            .one_or_none()
        )

        # Ensure object exists
        if obj:
            # Delete object and commit
            self._session.delete(obj)
            # Save changes
            self._session.commit()
        else:
            # Raise exception
            raise EquipmentNotFoundException(id)
