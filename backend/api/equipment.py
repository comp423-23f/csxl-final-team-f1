"""Equipment API

Equipment routes are used to create, retrieve, and update Equipment."""

from fastapi import APIRouter, Depends, HTTPException

from ..services.organization import OrganizationNotFoundException
from ..services.permission import UserPermissionException
from ..services import OrganizationService
from ..services import EquipmentService
from ..models.organization import Organization
from ..models.equipment import Equipment
from ..models.organization_details import OrganizationDetails
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


@api.post("", response_model=Equipment, tags=["Equipments"])
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
        # Try to create and return new organization
        return equipment_service.create(subject, equipment)
    except Exception as e:
        # Raise 422 exception if creation fails (request body is shaped incorrectly / not authorized)
        raise HTTPException(status_code=422, detail=str(e))


@api.get(
    "/{slug}",
    responses={404: {"model": None}},
    response_model=OrganizationDetails,
    tags=["Organizations"],
)
def get_organization_from_slug(
    slug: str, organization_service: OrganizationService = Depends()
) -> OrganizationDetails:
    """
    Get organization with matching slug

    Parameters:
        slug: a string representing a unique identifier for an Organization
        organization_service: a valid OrganizationService

    Returns:
        Organization: Organization with matching slug

    Raises:
        HTTPException 404 if get_from_slug() raises an Exception
    """

    # Try to get organization with matching slug
    try:
        # Return organization
        return organization_service.get_from_slug(slug)
    except OrganizationNotFoundException as e:
        # Raise 404 exception if search fails (no response)
        raise HTTPException(status_code=404, detail=str(e))


@api.put(
    "",
    responses={404: {"model": None}},
    response_model=Equipment,
    tags=["Equipments"],
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
        # Return updated organization
        return equipment_service.update(subject, equipment)
    except (OrganizationNotFoundException, UserPermissionException) as e:
        # Raise 404 exception if update fails (organization does not exist / not authorized)
        raise HTTPException(status_code=404, detail=str(e))


@api.delete("/{id}", response_model=None, tags=["Equipments"])
def delete_organization(
    id: num,
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
    except OrganizationNotFoundException as e:
        # Raise 404 exception if delete fails (organization does not exist / not authorized)
        raise HTTPException(status_code=404, detail=str(e))
