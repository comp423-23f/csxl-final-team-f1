"""Reservation Service manages equipment reservations for the XL."""

from fastapi import Depends
from datetime import datetime
from sqlalchemy.orm import Session
from ...database import db_session
from .equipment_reservation import EquipmentReservationService
from .equipment import EquipmentService
from .operating_hours import OperatingHoursService
from ...models.equipment import Status, TimeRange
from ...models import User
from .policy import PolicyService
from .operating_hours import OperatingHoursService


class StatusService:
    """RoleService is the access layer to the role data model, its members, and permissions."""

    def __init__(
        self,
        policies_svc: PolicyService = Depends(),
        operating_hours_svc: OperatingHoursService = Depends(),
        equipment_svc: EquipmentService = Depends(),
        reservation_svc: EquipmentReservationService = Depends(),
    ):
        self._policies_svc = policies_svc
        self._reservation_svc = reservation_svc
        self._operating_hours_svc = operating_hours_svc
        self._equipment_svc = equipment_svc

    def get_equipment_status(self, subject: User) -> Status:
        """All-in-one endpoint for a user to simultaneously get their own upcoming reservations and current status of the XL."""
        my_reservations = self._reservation_svc.get_current_reservations_for_user(
            subject, subject
        )

        now = datetime.now()
        walkin_window = TimeRange(
            start=now,
            end=now
            + self._policies_svc.walkin_window(subject)
            + 3 * self._policies_svc.walkin_initial_duration(subject),
            # We triple walkin duration for end bounds to find equipment not pre-reserved later. If XL stays
            # relatively open, the walkin could then more likely be extended while it is not busy.
            # This also prioritizes _not_ placing walkins in reservable equipment.
        )
        equipment = (
            self._equipment_svc.list()
        )  # All equipment are fair game for walkin purposes
        equipment_availability = self._reservation_svc.equipment_availability(
            equipment, walkin_window
        )

        operating_hours = self._operating_hours_svc.schedule(
            TimeRange(
                start=now, end=now + self._policies_svc.reservation_window(subject)
            )
        )

        return Status(
            my_reservations=my_reservations,
            equipment_availability=equipment_availability,
            operating_hours=operating_hours,
        )
