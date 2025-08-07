from datetime import date

from fastapi import HTTPException
from sqlalchemy import select, insert

from app.models import RoomsOrm
from app.models.bookings import BookingsOrm
from app.repositories.base import BaseRepository
from app.repositories.mappers.mappers import BookingDataMapper
from app.repositories.utils import rooms_ids_for_booking
from app.schemas.bookings import BookingAddRequest


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper

    async def get_bookings_with_today_chekin(self):
        query = (
            select(self.model)
            .filter(self.model.date_from == date.today())
        )
        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]

    async def add_booking(self, user_id: int, booking_data: BookingAddRequest):
        rooms_ids = rooms_ids_for_booking(date_from=booking_data.date_from, date_to=booking_data.date_to)
        rooms_ids_free = (await self.session.execute(rooms_ids)).scalars().all()
        print(rooms_ids_free)
        if booking_data.room_id not in rooms_ids_free:
            raise HTTPException(status_code=404, detail="Все номера заняты")
        query = select(RoomsOrm).filter_by(id=booking_data.room_id)
        room = (await self.session.execute(query)).scalar_one()
        add_data_stmt = insert(self.model).values(
            user_id=user_id,
            room_id=booking_data.room_id,
            date_from=booking_data.date_from,
            date_to=booking_data.date_to,
            price=room.price
        ).returning(self.model)

        result = await self.session.execute(add_data_stmt)
        model = result.scalar_one()
        return self.mapper.map_to_domain_entity(model)
