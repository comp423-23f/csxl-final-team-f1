"""Room models the essential information about a room in the equipment space."""

from pydantic import BaseModel


class Room(BaseModel):
    id: str
    nickname: str = ""
