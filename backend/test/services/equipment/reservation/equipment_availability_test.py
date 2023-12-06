"""ReservationService#equipment_availability tests"""

from .....services.equipment.equipment_reservation import (
    EquipmentReservationService,
    PolicyService,
)
from .....models.equipment import (
    TimeRange,
)

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
from .. import equipment_operating_hours_data
from .. import equipment_data
from . import equipment_reservation_data


def test_equipment_availability_in_past(
    reservation_svc: EquipmentReservationService, time: dict[str, datetime]
):
    """There is no equipment availability in the past."""
    past = TimeRange(start=time[THIRTY_MINUTES_AGO], end=time[NOW])
    available_equipment = reservation_svc.equipment_availability(
        equipment_data.equipment, past
    )
    assert len(available_equipment) == 0


def test_equipment_availability_beyond_scheduled_operating_hours(
    reservation_svc: EquipmentReservationService, time: dict[str, datetime]
):
    """When there are no operating hours in a given bounds, there is no availability."""
    out_of_bounds = TimeRange(
        start=time[NOW] + timedelta(days=423), end=time[NOW] + timedelta(days=424)
    )
    available_equipment = reservation_svc.equipment_availability(
        equipment_data.equipment, out_of_bounds
    )
    assert len(available_equipment) == 0


def test_equipment_availability_while_closed(
    reservation_svc: EquipmentReservationService,
):
    """There is no equipment availability while the XL is closed."""
    closed = TimeRange(
        start=equipment_operating_hours_data.today.end,
        end=equipment_operating_hours_data.today.end + ONE_HOUR,
    )
    available_equipment = reservation_svc.equipment_availability(
        equipment_data.equipment, closed
    )
    assert len(available_equipment) == 0


def test_equipment_availability_truncate_start(
    reservation_svc: EquipmentReservationService,
    policy_svc: PolicyService,
    time: dict[str, datetime],
):
    recent_past_to_five_minutes = TimeRange(
        start=time[NOW] - policy_svc.minimum_reservation_duration(),
        end=time[NOW] + FIVE_MINUTES,
    )
    available_equipment = reservation_svc.equipment_availability(
        equipment_data.equipment, recent_past_to_five_minutes
    )
    assert len(available_equipment) == 0


def test_equipment_availability_while_completely_open(
    reservation_svc: EquipmentReservationService,
):
    """All reservable equipment should be available."""
    tomorrow = TimeRange(
        start=equipment_operating_hours_data.future.start,
        end=equipment_operating_hours_data.future.start + ONE_HOUR,
    )
    available_equipment = reservation_svc.equipment_availability(
        equipment_data.reservable_equipment, tomorrow
    )
    assert len(available_equipment) == len(equipment_data.reservable_equipment)


def test_equipment_availability_with_reservation(
    reservation_svc: EquipmentReservationService, time: dict[str, datetime]
):
    """Test data has one of the reservable equipment reserved."""
    today = TimeRange(start=time[NOW], end=time[IN_THIRTY_MINUTES])
    available_equipment = reservation_svc.equipment_availability(
        equipment_data.reservable_equipment, today
    )
    assert len(available_equipment) == len(equipment_data.reservable_equipment) - 1
    assert available_equipment[0].id == equipment_data.vr3.id


def test_equipment_availability_near_requested_start(
    reservation_svc: EquipmentReservationService,
):
    """When the XL is open and some equipment are about to become available."""
    future = TimeRange(
        start=equipment_operating_hours_data.today.end - THIRTY_MINUTES - FIVE_MINUTES,
        end=equipment_operating_hours_data.today.end + FIVE_MINUTES,
    )
    available_equipment = reservation_svc.equipment_availability(
        equipment_data.reservable_equipment, future
    )
    assert len(available_equipment) == len(equipment_data.reservable_equipment)
    for equipment in available_equipment:
        assert (
            equipment.availability[0].start
            == equipment_reservation_data.reservation_4.end
        )
        assert equipment.availability[0].end == equipment_operating_hours_data.today.end


def test_equipment_availability_all_reserved(
    reservation_svc: EquipmentReservationService,
):
    """Test when all reservable equipment are reserved."""
    future = TimeRange(
        start=equipment_reservation_data.reservation_4.start,
        end=equipment_reservation_data.reservation_4.end,
    )
    available_equipment = reservation_svc.equipment_availability(
        equipment_data.reservable_equipment, future
    )
    assert len(available_equipment) == 0


def test_equipment_availability_xl_closing_soon(
    reservation_svc: EquipmentReservationService, policy_svc: PolicyService
):
    """When the XL is open and upcoming walkins are available, but the closing hour is under default walkin duration."""
    near_closing = TimeRange(
        start=equipment_operating_hours_data.tomorrow.end
        - (policy_svc.minimum_reservation_duration() - 2 * ONE_MINUTE),
        end=equipment_operating_hours_data.tomorrow.end,
    )
    available_equipment = reservation_svc.equipment_availability(
        equipment_data.equipment, near_closing
    )
    assert len(available_equipment) == 0
