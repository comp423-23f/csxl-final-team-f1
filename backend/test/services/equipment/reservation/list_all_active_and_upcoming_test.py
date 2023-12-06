"""ReservationService#list_all_active_and_upcoming tests."""

from unittest.mock import create_autospec

from .....services import PermissionService
from .....services.equipment import EquipmentReservationService

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


def test_list_all_active_and_upcoming(reservation_svc: EquipmentReservationService):
    all = reservation_svc.list_all_active_and_upcoming(user_data.ambassador)
    assert len(all) == len(equipment_reservation_data.active_reservations) + len(
        equipment_reservation_data.confirmed_reservations
    )


def test_list_all_active_and_upcoming_permission(
    reservation_svc: EquipmentReservationService,
):
    permission_svc = create_autospec(PermissionService)
    permission_svc.enforce.return_value = None
    reservation_svc._permission_svc = permission_svc
    reservation_svc.list_all_active_and_upcoming(user_data.ambassador)
    permission_svc.enforce.assert_called_once_with(
        user_data.ambassador,
        "equipment.reservation.read",
        f"user/*",
    )
