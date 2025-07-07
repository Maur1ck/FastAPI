from pydantic import BaseModel, Field


class FacilityAdd(BaseModel):
    title: str


class Facility(FacilityAdd):
    id: int
