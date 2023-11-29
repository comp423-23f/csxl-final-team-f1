"""Equipment data for tests."""

import pytest
from sqlalchemy import delete
from sqlalchemy.orm import Session
from ....entities.equipment import EquipmentEntity
from ....models.equipment.equipment import Equipment
from typing import Sequence

from ..reset_table_id_seq import reset_table_id_seq


vr1 = Equipment(
    id=1,
    name="VR Headset 1",
    reservable=True,
)

vr2: Equipment = Equipment(
    id=2,
    name="VR Headset 2",
    reservable=False,
)

vr3 = Equipment(
    id=3,
    name="VR Headset 3",
    reservable=True,
)

vr4 = Equipment(
    id=4,
    name="VR Headset 4",
    reservable=False,
)

keyboard1 = Equipment(id=20, name="Keyboard 1", reservable=False)

keyboard2 = Equipment(id=21, name="Keyboard 2", reservable=False)

keyboards = [keyboard1, keyboard2]

mouse1 = Equipment(id=40, name="Mouse 1", reservable=True)

mouse2 = Equipment(
    id=41,
    name="Mouse 2",
    reservable=False,
)

mouses = [mouse1, mouse2]

vr_headsets = [vr1, vr2, vr3, vr4]

equipments: Sequence[Equipment] = vr_headsets + keyboards + mouses

reservable_equipment = [equipment for equipment in equipments if equipment.reservable]

unreservable_equipment = [
    equipment for equipment in equipments if not equipment.reservable
]


def equipment_insert_fake_data(session: Session):
    for x in equipments:
        entity = EquipmentEntity.from_model(x)
        session.add(entity)
    reset_table_id_seq(
        session, EquipmentEntity, EquipmentEntity.id, len(equipments) + 1
    )


@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    equipment_insert_fake_data(session)
    session.commit()


def delete_all(session: Session):
    session.execute(delete(EquipmentEntity))
