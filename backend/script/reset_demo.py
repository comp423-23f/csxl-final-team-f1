import sys
from sqlalchemy import text
from sqlalchemy.orm import Session
from ..database import engine
from ..env import getenv
from .. import entities

from ..test.services import role_data, user_data, permission_data
from ..test.services.organization import organization_demo_data
from ..test.services.equipment import (
    equipment_data,
    equipment_operating_hours_data,
    equipment_time,
)
from ..test.services.equipment.reservation import equipment_reservation_data
from ..test.services.event import event_demo_data

from ..test.services.coworking import room_data, seat_data, operating_hours_data, time
from ..test.services.coworking.reservation import reservation_data

__authors__ = ["Kris Jordan", "Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

# Ensures that the script can only be run in development mode
if getenv("MODE") != "development":
    print("This script can only be run in development mode.", file=sys.stderr)
    print("Add MODE=development to your .env file in workspace's `backend/` directory")
    exit(1)

# Reset Tables
entities.EntityBase.metadata.drop_all(engine)
entities.EntityBase.metadata.create_all(engine)

# Initialize the SQLAlchemy session
with Session(engine) as session:
    # Load all demo data
    time = time.time_data()
    equipment_time = equipment_time.time_data()  # Ours
    role_data.insert_fake_data(session)
    user_data.insert_fake_data(session)
    permission_data.insert_fake_data(session)
    organization_demo_data.insert_fake_data(session)
    event_demo_data.insert_fake_data(session)
    operating_hours_data.insert_fake_data(session, time)
    equipment_operating_hours_data.equipment_insert_fake_data(
        session, equipment_time
    )  # Ours
    room_data.insert_fake_data(session)
    seat_data.insert_fake_data(session)
    reservation_data.insert_fake_data(session, time)
    equipment_data.equipment_insert_fake_data(session)  # Ours
    equipment_reservation_data.equipment_insert_fake_data(
        session, equipment_time
    )  # Ours

    # Commit changes to the database
    session.commit()
