"""Tests for Coworking Rooms Service."""

from ....services.equipment import EquipmentService

# Imported fixtures provide dependencies injected for the tests as parameters.
from .fixtures import equipment_svc

# Import the setup_teardown fixture explicitly to load entities in database
from .equipment_data import fake_data_fixture as insert_equipment_fake_data

# Import the fake model data in a namespace for test assertions
from . import equipment_data


def test_list(equipment_svc: EquipmentService):
    equipment = equipment_svc.list()
    assert len(equipment) == len(equipment_data.equipments)