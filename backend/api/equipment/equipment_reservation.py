"""Equipment Client Reservation API

This API is used to make and manage reservations."""

from fastapi import APIRouter, Depends, HTTPException
from ..authentication import registered_user
from ...services.equipment.equipment_reservation import EquipmentReservationService
from ...models import User
from ...models.equipment import (
    Reservation,
    ReservationRequest,
    ReservationPartial,
    ReservationState,
)

api = APIRouter(prefix="/api/equipment")
openapi_tags = {
    "name": "Equipment",
    "description": "Equipment reservations, status, and XL Ambassador functionality.",
}


@api.post("/reservation", tags=["Equipment"])
def draft_reservation(
    reservation_request: ReservationRequest,
    subject: User = Depends(registered_user),
    reservation_svc: EquipmentReservationService = Depends(),
) -> Reservation:
    """Draft a reservation request."""
    return reservation_svc.draft_reservation(subject, reservation_request)


@api.get("/reservation/{id}", tags=["Equipment"])
def get_reservation(
    id: int,
    subject: User = Depends(registered_user),
    reservation_svc: EquipmentReservationService = Depends(),
) -> Reservation:
    return reservation_svc.get_reservation(subject, id)


@api.put("/reservation/{id}", tags=["Equipment"])
def update_reservation(
    reservation: ReservationPartial,
    subject: User = Depends(registered_user),
    reservation_svc: EquipmentReservationService = Depends(),
) -> Reservation:
    """Modify a reservation."""
    return reservation_svc.change_reservation(subject, reservation)


@api.delete("/reservation/{id}", tags=["Equipment"])
def cancel_reservation(
    id: int,
    subject: User = Depends(registered_user),
    reservation_svc: EquipmentReservationService = Depends(),
) -> Reservation:
    """Cancel a reservation."""
    return reservation_svc.change_reservation(
        subject, ReservationPartial(id=id, state=ReservationState.CANCELLED)
    )
