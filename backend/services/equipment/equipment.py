"""Service that manages equipments in the equipment space."""

from fastapi import Depends
from sqlalchemy.orm import Session
from ...database import db_session
from ...models.equipment import Equipment
from ...models import User
from ...entities.equipment import EquipmentEntity
from ..permission import (
    PermissionService,
    PermissionEntity,
    Permission,
    UserPermissionException,
)

from ..exceptions import EquipmentNotFoundException
from ..exceptions import UserPermissionException


class EquipmentService:
    """EquipmentService is the access layer to equipment equipment."""

    def __init__(self, session: Session = Depends(db_session)):
        """Initializes a new RoomService.

        Args:
            session (Session): The database session to use, typically injected by FastAPI.
        """
        self._session = session

    def list(self) -> list[Equipment]:
        """Returns all equipments in the space.

        Returns:
            list[Equipment]: All equipment space orderd by increasing capacity.
        """
        entities = self._session.query(EquipmentEntity).all()
        return [entity.to_model() for entity in entities]

    # def create(self, subject: User, equipment: Equipment) -> Equipment:
    #     """
    #     Creates a organization based on the input object and adds it to the table.
    #     If the organization's ID is unique to the table, a new entry is added.
    #     If the organization's ID already exists in the table, it raises an error.

    #     Parameters:
    #         subject: a valid User model representing the currently logged in User
    #         organization (Organization): Organization to add to table

    #     Returns:
    #         Organization: Object added to table
    #     """

    #     # Check if user has admin permissions
    #     self._permission.enforce(subject, "equipment.create", f"equipment")

    #     # Checks if the organization already exists in the table
    #     if equipment.id:
    #         # Set id to None so database can handle setting the id
    #         equipment.id = None

    #     else:
    #         # Otherwise, create new object
    #         equipment_entity = EquipmentEntity.from_model(equipment)

    #         # Add new object to table and commit changes
    #         self._session.add(equipment_entity)
    #         self._session.commit()

    #         # Return added object
    #         return equipment_entity.to_model()

    # def update(self, subject: User, equipment: Equipment) -> Equipment:
    #     """
    #     Update the organization
    #     If none found with that id, a debug description is displayed.

    #     Parameters:
    #         subject: a valid User model representing the currently logged in User
    #         organization (Organization): Organization to add to table

    #     Returns:
    #         Organization: Updated organization object

    #     Raises:
    #         OrganizationNotFoundException: If no organization is found with the corresponding ID
    #     """

    #     # Check if user has admin permissions
    #     self._permission.enforce(subject, "organization.create", f"organization")

    #     # Query the organization with matching id
    #     obj = self._session.get(EquipmentEntity, equipment.id)

    #     # Check if result is null
    #     if obj:
    #         # Update organization object
    #         obj.name = equipment.name
    #         obj.reservable = equipment.reservable

    #         # Save changes
    #         self._session.commit()

    #         # Return updated object
    #         return obj.to_model()
    #     else:
    #         # Raise exception
    #         raise EquipmentNotFoundException(equipment.id)

    # def delete(self, subject: User, id: int) -> None:
    #     """
    #     Delete the organization based on the provided slug.
    #     If no item exists to delete, a debug description is displayed.

    #     Parameters:
    #         subject: a valid User model representing the currently logged in User
    #         slug: a string representing a unique organization slug

    #     Raises:
    #         OrganizationNotFoundException: If no organization is found with the corresponding slug
    #     """
    #     # Check if user has admin permissions
    #     self._permission.enforce(subject, "organization.create", f"organization")

    #     # Find object to delete
    #     obj = (
    #         self._session.query(EquipmentEntity)
    #         .filter(EquipmentEntity.id == id)
    #         .one_or_none()
    #     )

    #     # Ensure object exists
    #     if obj:
    #         # Delete object and commit
    #         self._session.delete(obj)
    #         # Save changes
    #         self._session.commit()
    #     else:
    #         # Raise exception
    #         raise EquipmentNotFoundException(id)
