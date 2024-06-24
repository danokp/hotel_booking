from pydantic import BaseModel


class HotelsSchema(BaseModel):
    id: int
    name: str
    location: str
    services: list[str]
    rooms_quantity: int
    image_id: int


class HotelsWithRoomsLeftSchema(HotelsSchema):
    rooms_left: int
