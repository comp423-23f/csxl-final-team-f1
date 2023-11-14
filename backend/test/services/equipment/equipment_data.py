"""Equipment data for tests."""

import pytest
from sqlalchemy import delete
from sqlalchemy.orm import Session
from ....entities.equipment import EquipmentEntity
from ....models.equipment.equipment_details import EquipmentDetails
from ....models.equipment.equipment import Equipment
from typing import Sequence

from ..reset_table_id_seq import reset_table_id_seq
from .room_data import the_xl

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

vr1 = EquipmentDetails(
    id=1,
    name="VR Headset 1",
    reservable=True,
    room=the_xl.to_room(),
)

vr2: Equipment = EquipmentDetails(
    id=2,
    name="VR Headset 2",
    reservable=False,
    room=the_xl.to_room(),
)

vr3 = EquipmentDetails(
    id=3,
    name="VR Headset 3",
    reservable=True,
    room=the_xl.to_room(),
)

vr4 = EquipmentDetails(
    id=4,
    name="VR Headset 4",
    reservable=False,
    room=the_xl.to_room(),
)

keyboard1 = EquipmentDetails(
    id=20, name="Keyboard 1", reservable=False, room=the_xl.to_room()
)

keyboard2 = EquipmentDetails(
    id=21, name="Keyboard 2", reservable=False, room=the_xl.to_room()
)

keyboards = [keyboard1, keyboard2]

mouse1 = EquipmentDetails(id=40, name="Mouse 1", reservable=True, room=the_xl.to_room())

mouse2 = EquipmentDetails(
    id=41,
    name="Mouse 2",
    reservable=False,
    room=the_xl.to_room(),
)

mouses = [mouse1, mouse2]

vr_headsets = [vr1, vr2, vr3, vr4]

equipment: Sequence[Equipment] = vr_headsets + keyboards + mouses

reservable_equipment = [equipment for equipment in equipment if equipment.reservable]

unreservable_equipment = [
    equipment for equipment in equipment if not equipment.reservable
]


def insert_fake_data(session: Session):
    for x in equipment:
        entity = EquipmentEntity.from_model(x)
        session.add(entity)
    reset_table_id_seq(session, EquipmentEntity, EquipmentEntity.id, len(equipment) + 1)


@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    insert_fake_data(session)
    session.commit()


def delete_all(session: Session):
    session.execute(delete(EquipmentEntity))
