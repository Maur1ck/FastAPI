from sqlalchemy import insert, select

from app.models.rooms import RoomsORM
from app.repositories.base import BaseRepository
from app.schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsORM
    schema = Room

    async def get_all(self, hotel_id: int):
        query = select(RoomsORM).where(RoomsORM.hotel_id == hotel_id)
        result = await self.session.execute(query)
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]

    async def add(self, data: dict):
        add_data_stmt = insert(self.model).values(**data).returning(self.model)
        result = await self.session.execute(add_data_stmt)
        model = result.scalar_one()
        return self.schema.model_validate(model, from_attributes=True)
