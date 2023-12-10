"""Test equipment StatusService"""

from .fixtures import status_svc
from ....services.equipment.status import StatusService
from ....models.equipment.availability import EquipmentAvailability
from datetime import timedelta

from ..core_data import user_data
from . import equipment_operating_hours_data
from .reservation import equipment_reservation_data

# Since there are relationship dependencies between the entities, order matters.
from .equipment_time import *
from ..core_data import setup_insert_data_fixture as insert_order_0
from .equipment_operating_hours_data import fake_data_fixture as insert_order_1
from .equipment_data import fake_data_fixture as insert_order_3
from .reservation.equipment_reservation_data import fake_data_fixture as insert_order_4


def test_status_dispatch(status_svc: StatusService):
    # Hard-wire mock responses to all dispatched methods
    # We test these methods elsewhere
    status_svc._reservation_svc.get_current_reservations_for_user.return_value = [
        equipment_reservation_data.reservation_1
    ]
    status_svc._policies_svc.walkin_window.return_value = timedelta(minutes=15)
    status_svc._policies_svc.walkin_initial_duration.return_value = timedelta(hours=1)
    status_svc._policies_svc.reservation_window.return_value = timedelta(weeks=1)
    status_svc._equipment_svc.list.return_value = []
    status_svc._operating_hours_svc.schedule.return_value = [
        equipment_operating_hours_data.today
    ]

    equipment_availability = [
        EquipmentAvailability(
            id=0,
            availability=[],
            name="S1",
            reservable=True,
            is_keyboard=True,
            is_mouse=False,
            is_vr=False,
        )
    ]
    status_svc._reservation_svc.equipment_availability.return_value = (
        equipment_availability
    )

    # Call the method
    status = status_svc.get_equipment_status(user_data.root)

    # Look for dependent methods to be called
    status_svc._reservation_svc.get_current_reservations_for_user.assert_called_once_with(
        user_data.root, user_data.root
    )
    status_svc._reservation_svc.equipment_availability.assert_called_once()
    status_svc._operating_hours_svc.schedule.assert_called_once()

    # Look for expected RVs
    assert status.my_reservations == [equipment_reservation_data.reservation_1]
    assert status.equipment_availability == equipment_availability
    assert status.operating_hours == [equipment_operating_hours_data.today]
