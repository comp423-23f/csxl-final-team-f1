"""Contains mock data for to run tests on the equipment feature."""

import pytest
from sqlalchemy.orm import Session
from ....models.equipment.equipment import Equipment
from ....entities.equipment.equipment_entity import EquipmentEntity

from ..reset_table_id_seq import reset_table_id_seq

# Sample Data Objects

vr1 = Equipment(
    id=1,
    name="Virtual Headset 1",
)

keyboard1 = Equipment(
    id=2,
    name="Keyboard 1",
)

mouse1 = EquipmentEntity(
    id=3,
    name="Mouse 1",
)

equipment = [vr1, keyboard1, mouse1]
equipment_names = [vr1.name, keyboard1.name, mouse1.name]

to_add = Equipment(
    name="Virtual Headset 2",
)

new_vr1 = Equipment(
    id=1,
    name="Virtual Headset 1",
)

# Data Functions


def insert_fake_data(session: Session):
    """Inserts fake equipment data into the test session."""

    global equipment

    # Create entities for test equipment data
    entities = []
    for x in equipment:
        entity = EquipmentEntity.from_model(x)
        session.add(entity)
        entities.append(entity)

    # Reset table IDs to prevent ID conflicts
    reset_table_id_seq(session, EquipmentEntity, EquipmentEntity.id, len(equipment) + 1)

    # Commit all changes
    session.commit()


@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    """Insert fake data the session automatically when test is run.
    Note:
        This function runs automatically due to the fixture property `autouse=True`.
    """
    insert_fake_data(session)
    session.commit()
    yield
