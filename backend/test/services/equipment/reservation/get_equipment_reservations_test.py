"""ReservationService#get_equipment_reservations tests."""

from unittest.mock import create_autospec

from .....models.equipment import (
    Reservation,
    TimeRange,
)
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


def test_get_equipment_reservations_none(
    reservation_svc: EquipmentReservationService, time: dict[str, datetime]
):
    """Get all reservations for a time range with no reservations."""
    in_the_past = TimeRange(
        start=time[THIRTY_MINUTES_AGO] - FIVE_MINUTES,
        end=time[THIRTY_MINUTES_AGO] - ONE_MINUTE,
    )
    reservations = reservation_svc.get_equipment_reservations(
        equipment_data.equipments, in_the_past
    )
    assert len(reservations) == 0


def test_get_equipment_reservations_active(
    reservation_svc: EquipmentReservationService, time: dict[str, datetime]
):
    """Get all reservations that are active (not cancelled or checked out)."""
    current = TimeRange(start=time[NOW], end=time[IN_THIRTY_MINUTES])
    reservations = reservation_svc.get_equipment_reservations(
        equipment_data.equipments, current
    )
    assert len(reservations) == len(equipment_reservation_data.active_reservations)
    assert isinstance(reservations[0], Reservation)
    assert reservations[0].id == equipment_reservation_data.reservation_1.id


def test_get_equipment_reservations_unreserved_equipments(
    reservation_svc: EquipmentReservationService, time: dict[str, datetime]
):
    """Get reservations for unreserved equipments (expecting no matches)."""
    current = TimeRange(start=time[NOW], end=time[IN_THIRTY_MINUTES])
    reservations = reservation_svc.get_equipment_reservations(
        equipment_data.unreservable_equipment, current
    )
    assert len(reservations) == 0
