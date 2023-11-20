"""ReservationService#get_equipment_reservations tests."""

from unittest.mock import create_autospec, call

from .....services.equipment import EquipmentReservationService
from .....services import PermissionService
from .....models.equipment import Reservation
from .....services.exceptions import ResourceNotFoundException, UserPermissionException
from .....services.equipment.equipment_reservation import ReservationException
from .....models.equipment import ReservationState

# Imported fixtures provide dependencies injected for the tests as parameters.
# Dependent fixtures (equipment_svc) are required to be imported in the testing module.
from ..fixtures import (
    reservation_svc,
    permission_svc,
    equipment_svc,
    policy_svc,
    operating_hours_svc,
)
from ..equipment_time import *

# Import the setup_teardown fixture explicitly to load entities in database.
# The order in which these fixtures run is dependent on their imported alias.
# Since there are relationship dependencies between the entities, order matters.
from ...core_data import setup_insert_data_fixture as insert_order_0
from ..equipment_operating_hours_data import fake_data_fixture as insert_order_1
from ..equipment_data import fake_data_fixture as insert_order_3
from .equipment_reservation_data import fake_data_fixture as insert_order_4

# Import the fake model data in a namespace for test assertions
from ...core_data import user_data
from .. import equipment_data
from . import equipment_reservation_data


def test_staff_checkin_success(
    reservation_svc: EquipmentReservationService,
):
    """Expected case of this service method."""
    reservation: Reservation = reservation_svc.staff_checkin_reservation(
        user_data.ambassador, equipment_reservation_data.reservation_4
    )
    assert reservation.id == equipment_reservation_data.reservation_4.id
    assert reservation.state == ReservationState.CHECKED_IN


def test_staff_checkin_idempotence(
    reservation_svc: EquipmentReservationService,
):
    """Repeated checkin requests should not error out and be idempotent."""
    reservation_svc.staff_checkin_reservation(
        user_data.ambassador, equipment_reservation_data.reservation_4
    )
    reservation: Reservation = reservation_svc.staff_checkin_reservation(
        user_data.ambassador, equipment_reservation_data.reservation_4
    )
    assert reservation.id == equipment_reservation_data.reservation_4.id
    assert reservation.state == ReservationState.CHECKED_IN


def test_staff_checkin_not_found(
    reservation_svc: EquipmentReservationService, time: dict[str, datetime]
):
    """ResourceNotFoundException expected when reservation does not exist."""
    reservation = Reservation(
        id=423,
        start=time[NOW],
        end=time[IN_ONE_HOUR],
        state=ReservationState.CONFIRMED,
        users=[],
        equipment=[],
        created_at=time[NOW],
        updated_at=time[NOW],
    )
    """Get an existing reservation as a user party to the reservation."""
    with pytest.raises(ResourceNotFoundException):
        reservation_svc.staff_checkin_reservation(user_data.ambassador, reservation)


def test_staff_checkin_wrong_state_draft(
    reservation_svc: EquipmentReservationService,
):
    """Checkins can only happen from a state of Confirmed."""
    with pytest.raises(ReservationException):
        reservation_svc.staff_checkin_reservation(
            user_data.ambassador, equipment_reservation_data.reservation_5
        )


def test_staff_checkin_wrong_state_checked_out(
    reservation_svc: EquipmentReservationService,
):
    """Checkins can only happen from a state of Confirmed."""
    with pytest.raises(ReservationException):
        reservation_svc.staff_checkin_reservation(
            user_data.ambassador, equipment_reservation_data.reservation_2
        )


def test_staff_checkin_wrong_state_cancelled(
    reservation_svc: EquipmentReservationService,
):
    """Checkins can only happen from a state of Confirmed."""
    with pytest.raises(ReservationException):
        reservation_svc.staff_checkin_reservation(
            user_data.ambassador, equipment_reservation_data.reservation_3
        )


def test_staff_checkin_enforces_permissions(
    reservation_svc: EquipmentReservationService,
):
    """Checkin requires a permission to take action equipment.reservation.manage on user/*"""
    permission_svc = create_autospec(PermissionService)
    permission_svc.enforce.return_value = None
    reservation_svc._permission_svc = permission_svc
    reservation = reservation_svc.staff_checkin_reservation(
        user_data.ambassador, equipment_reservation_data.reservation_4
    )
    assert reservation.id is not None
    permission_svc.enforce.assert_called_once_with(
        user_data.ambassador,
        "equipment.reservation.manage",
        "user/*",
    )
