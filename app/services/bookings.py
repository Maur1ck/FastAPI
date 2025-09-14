from app.schemas.bookings import BookingAddRequest, BookingAdd
from app.schemas.hotels import Hotel
from app.schemas.rooms import Room
from app.services.base import BaseService
from app.services.rooms import RoomService


class BookingService(BaseService):
    async def add_booking(self, user_id: int, booking_data: BookingAddRequest):
        room: Room = await RoomService(self.db).get_room_with_check(booking_data.room_id)
        hotel: Hotel = await self.db.hotels.get_one(id=room.hotel_id)
        room_price: int = room.price
        _booking_data = BookingAdd(
            user_id=user_id,
            price=room_price,
            **booking_data.model_dump(),
        )
        booking = await self.db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
        await self.db.commit()
        return booking

    async def get_bookings(self):
        return await self.db.bookings.get_all()

    async def get_my_bookings(self, user_id: int):
        return await self.db.bookings.get_filtered(user_id=user_id)
