from sqlalchemy import select, func

from app.models.hotels import HotelsORM
from app.repositories.base import BaseRepository


class HotelsRepository(BaseRepository):
    model = HotelsORM

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
        return result.scalars().all()
