"""Equipment Client Reservation API

This API is used to make and manage reservations."""

from fastapi import APIRouter, Depends, HTTPException
from ..authentication import registered_user
from ...services.coworking.reservation import ReservationService
from ...models import User
from ...models.equipment.reservation import Reservation, ReservationPartial

api = APIRouter(prefix="/api/coworking")
openapi_tags = {
    "name": "Coworking",
    "description": "Coworking reservations, status, and XL Ambassador functionality.",
}


@api.get("/reservation/{id}", tags=["Equipment"])
def get_reservation(
    id: int,
    subject: User = Depends(registered_user),
    reservation_svc: ReservationService = Depends(),
) -> Reservation:
    return reservation_svc.get_reservation(subject, id)  # type: ignore


@api.delete("/reservation/{id}", tags=["Coworking"])
def cancel_reservation(
    id: int,
    subject: User = Depends(registered_user),
    reservation_svc: ReservationService = Depends(),
) -> Reservation:
    """Cancel a reservation."""
    return reservation_svc.change_reservation(
        subject, ReservationPartial(id=id, state=ReservationState.CANCELLED)  # type: ignore
    )
