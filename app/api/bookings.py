from fastapi import APIRouter, Request

from app.api.dependencies import DBDep, UserIdDep
from app.schemas.bookings import BookingAdd, BookingAddRequest

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.post("")
async def create_booking(user_id: UserIdDep, booking_data: BookingAddRequest, db: DBDep):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    price = room.price
    _booking_data = BookingAdd(user_id=user_id, price=price, **booking_data.model_dump())
    booking = await db.bookings.add(_booking_data)
    await db.commit()
    return {"status": "OK", "data": booking}
