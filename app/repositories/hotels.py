from sqlalchemy import select, func

from app.models.hotels import HotelsORM
from app.models.rooms import RoomsORM
from app.repositories.base import BaseRepository
from app.repositories.utils import rooms_ids_for_booking
from app.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsORM
    schema = Hotel

    async def get_filtered_by_time(self, date_from, date_to, location, title, limit, offset):
        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to)
        hotels_ids_to_get = (
            select(RoomsORM.hotel_id)
            .select_from(RoomsORM)
            .filter(RoomsORM.id.in_(rooms_ids_to_get))
        )
        query =  select(self.model).filter(self.model.id.in_(hotels_ids_to_get))
        if title:
            query = query.filter(func.lower(HotelsORM.title).contains(title.strip().lower()))
        if location:
            query = query.filter(func.lower(HotelsORM.location).contains(location.strip().lower()))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]
