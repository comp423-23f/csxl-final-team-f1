"""Tests for the EquipmentService class."""

# PyTest
import pytest
from unittest.mock import create_autospec

from backend.services.equipment import EquipmentNotFoundException
from backend.services.exceptions import UserPermissionException

# Tested Dependencies
from ....models.equipment import Equipment
from ....services.equipment import EquipmentService

# Injected Service Fixtures
from ..fixtures import equipment_svc_integration

# Explicitly import Data Fixture to load entities in database
from ..core_data import setup_insert_data_fixture

# Data Models for Fake Data Inserted in Setup
from .equipment_test_data import (
    equipment,
    to_add,
    vr1,
    new_vr1,
)
from ..user_data import root, user

# Test Functions

# Test `EquipmentService.all()`


def test_get_all(equipment_svc_integration: EquipmentService):
    """Test that all equipment can be retrieved."""
    fetched_equipment = equipment_svc_integration.all()
    assert fetched_equipment is not None
    assert len(fetched_equipment) == len(equipment)
    assert isinstance(fetched_equipment[0], Equipment)


# Test `EquipmentService.get_from_id()`


def test_get_from_id(equipment_svc_integration: EquipmentService):
    """Test that equipment can be retrieved based on their ID."""
    fetched_equipment = equipment_svc_integration.get_from_id(1)
    assert fetched_equipment is not None
    assert isinstance(fetched_equipment, Equipment)
    assert fetched_equipment.id == vr1.id


# Test `EquipmentService.create()`


def test_create_enforces_permission(equipment_svc_integration: EquipmentService):
    """Test that the service enforces permissions when attempting to create an equipment."""

    # Setup to test permission enforcement on the PermissionService.
    equipment_svc_integration._permission = create_autospec(
        equipment_svc_integration._permission
    )

    # Test permissions with root user (admin permission)
    equipment_svc_integration.create(root, to_add)
    equipment_svc_integration._permission.enforce.assert_called_with(
        root, "equipment.create", "equipment"
    )


def test_create_equipment_as_root(equipment_svc_integration: EquipmentService):
    """Test that the root user is able to create new equipment."""
    created_equipment = equipment_svc_integration.create(root, to_add)
    assert created_equipment is not None
    assert created_equipment.id is not None


def test_create_equipment_as_user(equipment_svc_integration: EquipmentService):
    """Test that any user is *unable* to create new equipment."""
    with pytest.raises(UserPermissionException):
        equipment_svc_integration.create(user, to_add)
        pytest.fail()  # Fail test if no error was thrown above


# Test `EquipmentService.update()`
def test_update_equipment_as_root(
    equipment_svc_integration: EquipmentService,
):
    """Test that the root user is able to update equipment."""
    equipment_svc_integration.update(root, new_vr1)
    assert equipment_svc_integration.get_from_id(1).name == "Virtual Headset 1"


def test_update_equipment_as_user(equipment_svc_integration: EquipmentService):
    """Test that any user is *unable* to update new equipment."""
    with pytest.raises(UserPermissionException):
        equipment_svc_integration.update(user, new_vr1)


def test_delete_enforces_permission(equipment_svc_integration: EquipmentService):
    """Test that the service enforces permissions when attempting to delete an equipment."""

    # Setup to test permission enforcement on the PermissionService.
    equipment_svc_integration._permission = create_autospec(
        equipment_svc_integration._permission
    )

    # Test permissions with root user (admin permission)
    equipment_svc_integration.delete(root, 1)
    equipment_svc_integration._permission.enforce.assert_called_with(
        root, "equipment.create", "equipment"
    )


def test_delete_equipment_as_root(equipment_svc_integration: EquipmentService):
    """Test that the root user is able to delete equipment."""
    equipment_svc_integration.delete(root, 1)
    with pytest.raises(EquipmentNotFoundException):
        equipment_svc_integration.get_from_id(1)


def test_delete_equipment_as_user(equipment_svc_integration: EquipmentService):
    """Test that any user is *unable* to delete equipment."""
    with pytest.raises(UserPermissionException):
        equipment_svc_integration.delete(user, 1)
