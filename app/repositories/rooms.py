from sqlalchemy import select, func

from app.models.bookings import BookingsORM
from app.models.rooms import RoomsORM
from app.repositories.base import BaseRepository
from app.schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsORM
    schema = Room

    async def get_filtered_by_time(self, hotel_id, date_from, date_to):
        rooms_count = (
            select(BookingsORM.room_id, func.count("*").label("rooms_booked"))
            .select_from(BookingsORM)
            .filter(
                BookingsORM.date_from <= date_to,
                BookingsORM.date_to >= date_from
            )
            .group_by(BookingsORM.room_id)
            .cte(name="rooms_count")
        )

        rooms_left_table = (
            select(
                self.model.id.label("room_id"),
                (self.model.quantity - func.coalesce(rooms_count.c.rooms_booked, 0)).label("rooms_left")
            )
            .select_from(self.model)
            .outerjoin(rooms_count, self.model.id == rooms_count.c.room_id)
            .cte(name="rooms_left_table")
        )

        rooms_ids_for_hotel = (
            select(self.model.id)
            .select_from(self.model)
            .filter_by(hotel_id=hotel_id)
            .subquery(name="rooms_ids_for_hotel")
        )

        rooms_ids_to_get = (
            select(rooms_left_table.c.room_id)
            .select_from(rooms_left_table)
            .filter(
                rooms_left_table.c.rooms_left > 0,
                rooms_left_table.c.room_id.in_(rooms_ids_for_hotel),
            )
        )

        return await self.get_filtered(self.model.id.in_(rooms_ids_to_get))