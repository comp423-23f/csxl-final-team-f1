from pydantic import BaseModel


class Equipment(BaseModel):
    """
    Pydantic model to represent an `Equipment`.

    This model is based on the `EquipmentEntity` model, which defines the shape
    of the `Equipment` database in the PostgreSQL database.
    """

    id: int | None = None
    name: str
    reservable: bool
