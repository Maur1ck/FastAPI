from sqlalchemy import select, func

from app.models.hotels import HotelsORM
from app.repositories.base import BaseRepository
from app.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsORM
    schema = Hotel

    async def get_all(self, location, title, limit, offset):
        query = select(HotelsORM)
        if title:
            query = query.where(func.lower(HotelsORM.title).contains(title.strip().lower()))
        if location:
            query = query.where(func.lower(HotelsORM.location).contains(location.strip().lower()))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]
