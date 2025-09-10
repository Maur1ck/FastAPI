from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from sqlalchemy.orm import selectinload

from app.exceptions import RoomNotFoundException
from app.models.rooms import RoomsOrm
from app.repositories.base import BaseRepository
from app.repositories.mappers.mappers import RoomDataMapper, RoomDataWithRelsMapper
from app.repositories.utils import rooms_ids_for_booking
from app.schemas.rooms import Room


class RoomsRepository(BaseRepository[Room]):
    model = RoomsOrm
    mapper = RoomDataMapper

    async def get_filtered_by_time(self, hotel_id, date_from, date_to):
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities)) # type: ignore
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)
        return [
            RoomDataWithRelsMapper.map_to_domain_entity(model)
            for model in result.unique().scalars().all()
        ]

    async def get_one_with_rels(self, **filters):
        query = select(self.model).options(selectinload(self.model.facilities)).filter_by(**filters) # type: ignore
        result = await self.session.execute(query)
        try:
            model = result.scalars().one_or_none()
        except NoResultFound:
            raise RoomNotFoundException
        return RoomDataWithRelsMapper.map_to_domain_entity(model)
