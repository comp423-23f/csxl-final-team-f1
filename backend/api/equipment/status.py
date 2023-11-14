"""Equipment Status API

This API is used to retrieve and update a user's profile."""

from fastapi import APIRouter, Depends
from ..authentication import registered_user
from ...services.equipment import StatusService
from ...models import User
from ...models.equipment import Status


api = APIRouter(prefix="/api/equipment/status")
openapi_tags = {
    "name": "Equipment",
    "description": "The XL's equipment are reserved and managed via these endpoints.",
}


@api.get("", response_model=Status, tags=["Equipment"])
def get_equipment_status(
    subject: User = Depends(registered_user), status_svc: StatusService = Depends()
):
    """Status endpoint supports the primary screen of the equipment features.

    It returns information about upcoming, active reservations the subject holds.
    It also fetches the current seat availability of the XL during operating hours.
    Finally, it provides a list of upcoming hours.
    """
    return status_svc.get_equipment_status(subject)
