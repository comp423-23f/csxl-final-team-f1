"""Definition of SQLAlchemy table-backed object mapping entity for Organizations."""

from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .entity_base import EntityBase
from typing import Self
from ..models.equipment import Equipment

# from ..models.organization_details import OrganizationDetails


class EquipmentEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `Organization` table"""

    # Name for the equipment table in the PostgreSQL database
    __tablename__ = "equipment"

    # Equipment properties (columns in the database table)

    # Unique ID for the device
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # Name of the device
    name: Mapped[str] = mapped_column(String, nullable=False, default="")

    @classmethod
    def from_model(cls, model: Equipment) -> Self:
        """
        Class method that converts an `Organization` model into a `OrganizationEntity`

        Parameters:
            - model (Organization): Model to convert into an entity
        Returns:
            OrganizationEntity: Entity created from model
        """
        return cls(
            id=model.id,
            name=model.name,
        )

    def to_model(self) -> Equipment:
        """
        Converts a `OrganizationEntity` object into a `Organization` model object

        Returns:
            Organization: `Organization` object from the entity
        """
        return Equipment(
            id=self.id,
            name=self.name,
        )

    # def to_details_model(self) -> OrganizationDetails:
    #     """
    #     Converts a `OrganizationEntity` object into a `OrganizationDetails` model object

    #     Returns:
    #         OrganizationDetails: `OrganizationDetails` object from the entity
    #     """
    #     return OrganizationDetails(
    #         id=self.id,
    #         name=self.name,
    #         shorthand=self.shorthand,
    #         slug=self.slug,
    #         logo=self.logo,
    #         short_description=self.short_description,
    #         long_description=self.long_description,
    #         website=self.website,
    #         email=self.email,
    #         instagram=self.instagram,
    #         linked_in=self.linked_in,
    #         youtube=self.youtube,
    #         heel_life=self.heel_life,
    #         public=self.public,
    #         events=[event.to_model() for event in self.events],
    #     )
