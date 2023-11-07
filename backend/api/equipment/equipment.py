"""Equipment API

Equipment routes are used to create, retrieve, and update Equipment.
"""

from fastapi import APIRouter, Depends, HTTPException

from ...services import EquipmentService
from ...models.equipment import Equipment
from ..authentication import registered_user
from ...models.user import User

api = APIRouter(prefix="/api/equipment")


@api.get("", response_model=list[Equipment], tags=["Equipment"])
def get_equipment(
    equipment_service: EquipmentService = Depends(),
) -> list[Equipment]:
    return equipment_service.all()


# @api.post("", response_model=Equipment, tags=["Equipment"])
# def new_equipment(
#     equipment: Equipment,
#     subject: User = Depends(registered_user),
#     equipment_service: EquipmentService = Depends(),
# ) -> Equipment:
#     try:
#         return equipment_service.create(subject, equipment)
#     except Exception as e:
#         raise HTTPException(status_code=422, detail=str(e))


# @api.put(
#     "", responses={404: {"model": None}}, response_model=Equipment, tags=["Equipment"]
# )
# def update_equipment(
#     equipment: Equipment,
#     subject: User = Depends(registered_user),
#     equipment_service: EquipmentService = Depends(),
# ) -> Equipment:
#     try:
#         return equipment_service.update(subject, equipment)
#     except Exception as e:
#         raise HTTPException(status_code=422, detail=str(e))


# @api.delete("/{id}", response_model=None, tags=["Equipment"])
# def delete_equipment(
#     id: int,
#     subject: User = Depends(registered_user),
#     equipment_service: EquipmentService = Depends(),
# ):
#     try:
#         equipment_service.delete(subject, id)  # type: ignore
#     except Exception as e:
#         raise HTTPException(status_code=422, detail=str(e))
