"""Fixtures used for testing the Coworking Services."""

import pytest
from unittest.mock import create_autospec
from sqlalchemy.orm import Session
from ....services import PermissionService
from ....services.equipment import (
    EquipmentService,
    EquipmentReservationService,
    PolicyService,
    StatusService,
)
from ....services.equipment.operating_hours import OperatingHoursService


@pytest.fixture()
def permission_svc(session: Session):
    """PermissionService fixture."""
    return PermissionService(session)


@pytest.fixture()
def operating_hours_svc(session: Session):
    """OperatingHoursService fixture."""
    return OperatingHoursService(session)


@pytest.fixture()
def equipment_svc(session: Session):
    """EquipmentService fixture."""
    return EquipmentService(session)


@pytest.fixture()
def policy_svc():
    """EquipmentPolicyService fixture."""
    return PolicyService()


@pytest.fixture()
def reservation_svc(
    session: Session,
    policy_svc: PolicyService,
    permission_svc: PermissionService,
    operating_hours_svc: OperatingHoursService,
    equipment_svc: EquipmentService,
):
    """ReservationService fixture."""
    return EquipmentReservationService(
        session, permission_svc, policy_svc, operating_hours_svc, equipment_svc
    )


@pytest.fixture()
def status_svc():
    policies_mock = create_autospec(PolicyService)
    operating_hours_mock = create_autospec(OperatingHoursService)
    equipment_mock = create_autospec(EquipmentService)
    reservation_mock = create_autospec(EquipmentReservationService)
    return StatusService(
        policies_mock, operating_hours_mock, equipment_mock, reservation_mock
    )
