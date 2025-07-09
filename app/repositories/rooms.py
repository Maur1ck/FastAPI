from sqlalchemy import select, func

from sqlalchemy.orm import selectinload, joinedload

from app.models.rooms import RoomsOrm
from app.repositories.base import BaseRepository
from app.repositories.utils import rooms_ids_for_booking
from app.schemas.rooms import Room, RoomWithRels


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_filtered_by_time(self, hotel_id, date_from, date_to):
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)
        return [RoomWithRels.model_validate(model, from_attributes=True) for model in result.unique().scalars().all()]
