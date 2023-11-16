"""Contains mock data for the live demo of the equipment feature."""

import pytest
from sqlalchemy.orm import Session
from ....models.equipment import Equipment
from ....entities.equipment_entity import EquipmentEntity
from ..reset_table_id_seq import reset_table_id_seq

# Sample Data Objects

vr1 = Equipment(
    id=1,
    name="VR Headset 1",
    reservable=True,
)

vr2 = Equipment(
    id=2,
    name="VR Headset 2",
    reservable=True,
)

vr3 = Equipment(
    id=3,
    name="VR Headset 3",
    reservable=True,
)

vr4 = Equipment(
    id=4,
    name="VR Headset 4",
    reservable=True,
)

keyboard1 = Equipment(
    id=5,
    name="Keyboard 1",
    reservable=True,
)

keyboard2 = Equipment(
    id=6,
    name="Keyboard 2",
    reservable=True,
)

keyboard3 = Equipment(
    id=7,
    name="Keyboard 3",
    reservable=True,
)

keyboard4 = Equipment(
    id=8,
    name="Keyboard 4",
    reservable=True,
)

mouse1 = Equipment(
    id=9,
    name="Mouse 1",
    reservable=True,
)

mouse2 = Equipment(
    id=10,
    name="Mouse 2",
    reservable=True,
)

mouse3 = Equipment(
    id=11,
    name="Mouse 3",
    reservable=True,
)

mouse4 = Equipment(
    id=12,
    name="Mouse 4",
    reservable=True,
)

equipment = [
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
    """Inserts fake equipment data into the test session."""

    global equipment

    # Create entities for test equipment data
    entities = []
    for x in equipment:
        # Equipment uses from_model, not sure why we have to use to_model
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
