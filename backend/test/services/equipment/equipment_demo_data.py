"""Contains mock data for the live demo of the equipment feature."""

import pytest
from sqlalchemy.orm import Session
from ....models.equipment import Equipment
from ....entities.equipment_entity import EquipmentEntity
from ..reset_table_id_seq import reset_table_id_seq

# Sample Data Objects

vr1 = EquipmentEntity(
    id=1,
    name="VR Headset 1",
)

vr2 = EquipmentEntity(
    id=2,
    name="VR Headset 2",
)

vr3 = EquipmentEntity(
    id=3,
    name="VR Headset 3",
)

vr4 = EquipmentEntity(
    id=4,
    name="VR Headset 4",
)

keyboard1 = EquipmentEntity(
    id=5,
    name="Keyboard 1",
)

keyboard2 = EquipmentEntity(
    id=6,
    name="Keyboard 2",
)

keyboard3 = EquipmentEntity(
    id=7,
    name="Keyboard 3",
)

keyboard4 = EquipmentEntity(
    id=8,
    name="Keyboard 4",
)

mouse1 = EquipmentEntity(
    id=9,
    name="Mouse 1",
)

mouse2 = EquipmentEntity(
    id=10,
    name="Mouse 2",
)

mouse3 = EquipmentEntity(
    id=11,
    name="Mouse 3",
)

mouse4 = EquipmentEntity(
    id=12,
    name="Mouse 4",
)

equipments = [
    vr1,
    vr2,
    vr3,
    vr4,
    keyboard1,
    keyboard2,
    keyboard3,
    keyboard4,
    mouse1,
    mouse2,
    mouse3,
    mouse4,
]

# Data Functions


def insert_fake_data(session: Session):
    """Inserts fake organization data into the test session."""

    global equipments

    # Create entities for test organization data
    entities = []
    for equipment in equipments:
        # Organization uses from_model, not sure why we have to use to_model
        entity = EquipmentEntity.to_model(equipment)
        session.add(entity)
        entities.append(entity)

    # Reset table IDs to prevent ID conflicts
    reset_table_id_seq(
        session, EquipmentEntity, EquipmentEntity.id, len(equipments) + 1
    )

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
