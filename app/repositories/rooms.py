from sqlalchemy import select, func

from app.models.bookings import BookingsOrm
from app.models.rooms import RoomsOrm
from app.repositories.base import BaseRepository
from app.repositories.utils import rooms_ids_for_booking
from app.schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_filtered_by_time(self, hotel_id, date_from, date_to):
        rooms_ids_to_get = rooms_ids_for_booking(hotel_id, date_from, date_to)
        return await self.get_filtered(self.model.id.in_(rooms_ids_to_get))
