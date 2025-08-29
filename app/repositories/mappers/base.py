from typing import TypeVar, Generic

from pydantic import BaseModel

from app.database import Base


SchemaType = TypeVar("SchemaType", bound=BaseModel)


class DataMapper(Generic[SchemaType]):
    db_model: type[Base]
    schema: type[SchemaType]

    @classmethod
    def map_to_domain_entity(cls, data) -> SchemaType:
        return cls.schema.model_validate(data, from_attributes=True)

    @classmethod
    def map_to_persistence_entity(cls, data) -> Base:
        return cls.db_model(**data.model_dump())
