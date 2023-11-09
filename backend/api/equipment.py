"""Equipment API

Equipment routes are used to create, retrieve, and update Equipment."""

from fastapi import APIRouter, Depends, HTTPException

from ..services.equipment import EquipmentNotFoundException
from ..services.permission import UserPermissionException
from ..services import OrganizationService
from ..services.equipment import EquipmentService
from ..models.equipment import Equipment
from ..api.authentication import registered_user
from ..models.user import User

api = APIRouter(prefix="/api/equipment")
openapi_tags = {
    "name": "Equipment",
    "description": "Create, update, delete, and retrieve Equipment.",
}


@api.get("", response_model=list[Equipment], tags=["Equipment"])
def get_equipment(
    equipment_service: EquipmentService = Depends(),
) -> list[Equipment]:
    """
    Get all equipment

    Parameters:
        equipment_service: a valid EquipmentService

    Returns:
        list[Equipment]: All `Equipment`s in the `Equipment` database table
    """

    # Return all equipment
    return equipment_service.all()


@api.post("", response_model=Equipment, tags=["Equipment"])
def new_equipment(
    equipment: Equipment,
    subject: User = Depends(registered_user),
    equipment_service: EquipmentService = Depends(),
) -> Equipment:
    """
    Create Equipment

    Parameters:
        equipment: a valid Equipment model
        subject: a valid User model representing the currently logged in User
        equipment_service: a valid EquipmentService

    Returns:
        Equipment: Created equipment

    Raises:
        HTTPException 422 if create() raises an Exception
    """

    try:
        # Try to create and return new equipment
        return equipment_service.create(subject, equipment)
    except Exception as e:
        # Raise 422 exception if creation fails (request body is shaped incorrectly / not authorized)
        raise HTTPException(status_code=422, detail=str(e))


@api.get(
    "/{id}",
    responses={404: {"model": None}},
    response_model=Equipment,
    tags=["Equipment"],
)
def get_equipment_from_id(
    id: int, equipment_service: EquipmentService = Depends()
) -> Equipment:
    """
    Get equipment with matching id

    Parameters:
        id: an int representing a unique identifier for an Equipment
        equipment_service: a valid EquipmentService

    Returns:
        Equipment: Equipment with matching id

    Raises:
        HTTPException 404 if get_equipment_from_id() raises an Exception
    """

    # Try to get equipment with matching id
    try:
        # Return equipment
        return equipment_service.get_from_id(id)
    except EquipmentNotFoundException as e:
        # Raise 404 exception if search fails (no response)
        raise HTTPException(status_code=404, detail=str(e))


@api.put(
    "",
    responses={404: {"model": None}},
    response_model=Equipment,
    tags=["Equipment"],
)
def update_equipment(
    equipment: Equipment,
    subject: User = Depends(registered_user),
    equipment_service: EquipmentService = Depends(),
) -> Equipment:
    """
    Update equipment

    Parameters:
        equipment: a valid Equipment model
        subject: a valid User model representing the currently logged in User
        equipment_service: a valid EquipmentService

    Returns:
        Equipment: Updated equipment

    Raises:
        HTTPException 404 if update() raises an Exception
    """
    try:
        # Return updated equipment
        return equipment_service.update(subject, equipment)
    except (EquipmentNotFoundException, UserPermissionException) as e:
        # Raise 404 exception if update fails (equipment does not exist / not authorized)
        raise HTTPException(status_code=404, detail=str(e))


@api.delete("/{id}", response_model=None, tags=["Equipment"])
def delete_equipment(
    id: int,
    subject: User = Depends(registered_user),
    equipment_service=Depends(EquipmentService),
):
    """
    Delete Equipment based on id

    Parameters:
        id: a num representing a unique identifier for an Equipment
        subject: a valid User model representing the currently logged in User
        equipment_service: a valid EquipmentService

    Raises:
        HTTPException 404 if delete() raises an Exception
    """

    try:
        # Try to delete equipment
        equipment_service.delete(subject, id)
    except EquipmentNotFoundException as e:
        # Raise 404 exception if delete fails (equipment does not exist / not authorized)
        raise HTTPException(status_code=404, detail=str(e))
