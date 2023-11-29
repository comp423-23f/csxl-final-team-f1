"""ReservationService#draft_reservation method tests"""

import pytest
from unittest.mock import create_autospec

from .....services import PermissionService
from .....services.equipment import EquipmentReservationService
from .....services.equipment.equipment_reservation import ReservationException
from .....models.equipment import ReservationState

from .....models.user import UserIdentity
from .....models.equipment.equipment import EquipmentIdentity

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

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


def test_draft_reservation_open_equipment(
    reservation_svc: EquipmentReservationService, time: dict[str, datetime]
):
    """Request with an open equipment."""
    reservation = reservation_svc.draft_reservation(
        user_data.ambassador, equipment_reservation_data.test_request()
    )
    assert reservation is not None
    assert reservation.id is not None
    assert reservation.state == ReservationState.DRAFT
    assert_equal_times(time[NOW], reservation.start)
    assert_equal_times(time[IN_THIRTY_MINUTES], reservation.end)
    assert_equal_times(time[NOW], reservation.created_at)
    assert_equal_times(time[NOW], reservation.updated_at)
    # assert len(reservation.equipment) == 1
    # assert len(reservation.users) == 1
    # assert reservation.users[0].id == user_data.ambassador.id


def test_draft_reservation_in_past(
    reservation_svc: EquipmentReservationService, time: dict[str, datetime]
):
    """Request a reservation that starts in the past. Its start should be now, instead."""
    reservation = reservation_svc.draft_reservation(
        user_data.ambassador,
        equipment_reservation_data.test_request({"start": time[THIRTY_MINUTES_AGO]}),
    )
    assert_equal_times(time[NOW], reservation.start)


def test_draft_reservation_beyond_walkin_limit(
    reservation_svc: EquipmentReservationService,
):
    """Walkin time limit should be bounded by PolicyService#walkin_initial_duration"""
    reservation = reservation_svc.draft_reservation(
        user_data.user,
        equipment_reservation_data.test_request(
            {
                "users": [UserIdentity(**user_data.user.model_dump())],
                "start": equipment_reservation_data.reservation_1.end,
                "end": equipment_reservation_data.reservation_1.end
                + reservation_svc._policy_svc.walkin_initial_duration(user_data.user)
                + timedelta(minutes=10),
            }
        ),
    )
    assert_equal_times(equipment_reservation_data.reservation_1.end, reservation.start)
    assert_equal_times(
        equipment_reservation_data.reservation_1.end
        + reservation_svc._policy_svc.walkin_initial_duration(user_data.user),
        reservation.end,
    )


# def test_draft_reservation_some_taken_equipment(
#     reservation_svc: EquipmentReservationService,
# ):
#     """Request with list of some taken, some open equipment."""
#     reservation = reservation_svc.draft_reservation(
#         user_data.ambassador,
#         reservation_data.test_request(
#             {
#                 "equipment": [
#                     EquipmentIdentity(
#                         **reservation_data.reservation_1.equipment[0].model_dump()
#                     ),
#                     EquipmentIdentity(**equipment_data.vr2.model_dump()),
#                 ]
#             }
#         ),
#     )
#     assert len(reservation.equipment) == 1
#     assert reservation.equipment[0].id == equipment_data.vr2.id


# def test_draft_reservation_equipment_availability_truncated(
#     reservation_svc: EquipmentReservationService,
# ):
#     """When walkin requested and equipment is reserved later on."""
#     reservation = reservation_svc.draft_reservation(
#         user_data.user,
#         reservation_data.test_request(
#             {
#                 "users": [UserIdentity(**user_data.user.model_dump())],
#                 "start": reservation_data.reservation_1.end,
#                 "end": operating_hours_data.today.end,
#                 "equipment": [
#                     EquipmentIdentity(**equipment.model_dump())
#                     for equipment in reservation_data.reservation_4.equipment
#                 ],
#             }
#         ),
#     )
#     assert_equal_times(reservation_data.reservation_4.start, reservation.end)
#     assert len(reservation.equipment) == 1


def test_draft_reservation_future(reservation_svc: EquipmentReservationService):
    """When a reservation is in the future, it has longer limits."""
    future_reservation_limit = (
        reservation_svc._policy_svc.maximum_initial_reservation_duration(user_data.user)
    )
    start = equipment_operating_hours_data.future.start
    end = equipment_operating_hours_data.future.start + future_reservation_limit
    reservation = reservation_svc.draft_reservation(
        user_data.user,
        equipment_reservation_data.test_request(
            {
                "users": [UserIdentity(**user_data.user.model_dump())],
                "equipment": [
                    EquipmentIdentity(**equipment.model_dump())
                    for equipment in equipment_data.reservable_equipment
                ],
                "start": start,
                "end": end,
            }
        ),
    )
    assert_equal_times(start, reservation.start)
    assert_equal_times(end, reservation.end)


def test_draft_reservation_future_unreservable(
    reservation_svc: EquipmentReservationService,
):
    """When a reservation is not a walk-in, only unreservable equipment are available."""
    with pytest.raises(ReservationException):
        start = equipment_operating_hours_data.tomorrow.start
        end = equipment_operating_hours_data.tomorrow.start + ONE_HOUR
        reservation = reservation_svc.draft_reservation(
            user_data.ambassador,
            equipment_reservation_data.test_request(
                {
                    "equipment": [
                        EquipmentIdentity(**equipment.model_dump())
                        for equipment in equipment_data.unreservable_equipment
                    ],
                    "start": start,
                    "end": end,
                }
            ),
        )


# def test_draft_reservation_all_closed_equipment(
#     reservation_svc: EquipmentReservationService,
# ):
#     """Request with all closed equipment errors."""
#     with pytest.raises(ReservationException):
#         reservation = reservation_svc.draft_reservation(
#             user_data.ambassador,
#             reservation_data.test_request(
#                 {
#                     "equipment": [
#                         EquipmentIdentity(
#                             **reservation_data.reservation_1.equipment[0].model_dump()
#                         ),
#                     ]
#                 }
#             ),
#         )


def test_draft_reservation_has_reservation_conflict(
    reservation_svc: EquipmentReservationService,
):
    with pytest.raises(ReservationException):
        reservation = reservation_svc.draft_reservation(
            user_data.user,
            equipment_reservation_data.test_request(
                {"users": [UserIdentity(**user_data.user.model_dump())]}
            ),
        )


def test_draft_walkin_reservation_has_walkin_reservation_conflict(
    reservation_svc: EquipmentReservationService, time: dict[str, datetime]
):
    """If conflicting reservation is another walkin, a ReservationException is raised."""
    reservation = reservation_svc.draft_reservation(
        user_data.ambassador,
        equipment_reservation_data.test_request({"start": time[THIRTY_MINUTES_AGO]}),
    )
    assert reservation.walkin
    with pytest.raises(ReservationException):
        # Repeat request
        reservation = reservation_svc.draft_reservation(
            user_data.ambassador,
            equipment_reservation_data.test_request(
                {"start": time[THIRTY_MINUTES_AGO]}
            ),
        )


def test_draft_reservation_in_middle_of_another(
    reservation_svc: EquipmentReservationService, time: dict[str, datetime]
):
    """If conflicting reservation is in the middle of another reservation the user has a ReservationError is expected."""
    with pytest.raises(ReservationException):
        # Conflict request
        reservation_svc.draft_reservation(
            user_data.ambassador,
            equipment_reservation_data.test_request(
                {
                    "start": equipment_operating_hours_data.today.end
                    - ONE_HOUR
                    + FIVE_MINUTES,
                    "end": equipment_operating_hours_data.today.end
                    - ONE_HOUR
                    + FIVE_MINUTES * 4,
                }
            ),
        )


def test_draft_reservation_has_conflict_but_ok(
    reservation_svc: EquipmentReservationService, time: dict[str, datetime]
):
    """This test case is for when a user has a reservation in the future (say in 30 minutes) and
    wants to make a drop-in visit right now, leading up to the reservation. Since the initial request
    is for one-hour, we need to check that the drop-in appointment is truncated to just _before_
    the next reservation begins."""
    conflict = equipment_reservation_data.reservation_4
    reservation = reservation_svc.draft_reservation(
        user_data.root,
        equipment_reservation_data.test_request(
            {
                "start": time[NOW],
                "end": conflict.start + THIRTY_MINUTES,
                "users": [UserIdentity(**user_data.root.model_dump())],
            }
        ),
    )
    assert reservation.id is not None
    assert_equal_times(conflict.start, reservation.end)


def test_draft_reservation_has_no_users(reservation_svc: EquipmentReservationService):
    with pytest.raises(ReservationException):
        reservation = reservation_svc.draft_reservation(
            user_data.user, equipment_reservation_data.test_request({"users": []})
        )


def test_draft_reservation_permissions(reservation_svc: EquipmentReservationService):
    permission_svc = create_autospec(PermissionService)
    permission_svc.enforce.return_value = None
    reservation_svc._permission_svc = permission_svc
    reservation = reservation_svc.draft_reservation(
        user_data.root, equipment_reservation_data.test_request()
    )
    assert reservation.id is not None
    permission_svc.enforce.assert_called_once_with(
        user_data.root,
        "equipment.reservation.manage",
        f"user/{user_data.ambassador.id}",
    )


def test_draft_reservation_multiple_users_not_implemented(
    reservation_svc: EquipmentReservationService,
):
    with pytest.raises(NotImplementedError):
        reservation_svc.draft_reservation(
            user_data.ambassador,
            equipment_reservation_data.test_request(
                {
                    "users": [
                        UserIdentity(**user_data.root.model_dump()),
                        UserIdentity(**user_data.ambassador.model_dump()),
                    ]
                }
            ),
        )
