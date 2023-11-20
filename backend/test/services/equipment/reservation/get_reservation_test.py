"""ReservationService#get_equipment_reservations tests."""

from unittest.mock import create_autospec, call

from .....services.equipment import EquipmentReservationService
from .....services import PermissionService
from .....models.equipment import Reservation
from .....services.exceptions import ResourceNotFoundException, UserPermissionException

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


def test_get_reservation(
    reservation_svc: EquipmentReservationService,
):
    """Get an existing reservation as a user party to the reservation."""
    reservation: Reservation = reservation_svc.get_reservation(
        user_data.user, equipment_reservation_data.reservation_1.id
    )
    assert reservation.id == equipment_reservation_data.reservation_1.id
    assert reservation.start == equipment_reservation_data.reservation_1.start
    # assert user_data.user.id in [u.id for u in reservation.users]


def test_get_non_existent_reservation(
    reservation_svc: EquipmentReservationService,
):
    """Get an existing reservation as a user party to the reservation."""
    with pytest.raises(ResourceNotFoundException):
        NONEXISTENT_ID = 423
        reservation: Reservation = reservation_svc.get_reservation(
            user_data.user, NONEXISTENT_ID
        )


def test_get_reservation_enforces_permissions(
    reservation_svc: EquipmentReservationService,
):
    permission_svc = create_autospec(PermissionService)
    permission_svc.check.return_value = False
    reservation_svc._permission_svc = permission_svc
    with pytest.raises(UserPermissionException):
        reservation_svc.get_reservation(
            user_data.user, equipment_reservation_data.reservation_4.id
        )
        calls = [
            call(
                user_data.user,
                "equipment.reservation.read",
                f"user/{equipment_reservation_data.reservation_4.users[0].id}",
            ),
            call(
                user_data.user,
                "equipment.reservation.read",
                f"user/{equipment_reservation_data.reservation_4.users[1].id}",
            ),
        ]
        permission_svc.check.assert_has_calls(calls)
