"""Contains mock data for to run tests on the equipment feature."""

import pytest
from sqlalchemy.orm import Session
from ....models.equipment import Equipment
from ....entities.equipment_entity import EquipmentEntity

from ..reset_table_id_seq import reset_table_id_seq

# Sample Data Objects

vr1 = Equipment(
    id=1,
    name="Virtual Headset 1",
    image="https://s7d1.scene7.com/is/image/dmqualcommprod/meta-quest-3-4?$QC_Responsive$&fmt=png-alpha",
)

keyboard1 = Equipment(
    id=2,
    name="Keyboard 1",
    image="https://pngimg.com/uploads/keyboard/keyboard_PNG101845.png",
)

mouse1 = Equipment(
    id=3,
    name="Mouse 1",
    image="https://purepng.com/public/uploads/large/one-rat-p5i.png",
)

invalidTester = Equipment(
    id=99999,
    name="Invalid Test Equipment",
    image="https://simonhwalkerdotcom.files.wordpress.com/2019/05/73927540-invalid-rubber-stamp-grunge-design-with-dust-scratches-effects-can-be-easily-removed-for-a-clean-cri.jpg",
)


equipment = [vr1, keyboard1, mouse1]
equipment_names = [vr1.name, keyboard1.name, mouse1.name]

# to_add = Equipment(
#     name="Virtual Headset 2",
# )

# new_vr1 = Equipment(
#     id=1,
#     name="Virtual Headset 1",
# )

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
