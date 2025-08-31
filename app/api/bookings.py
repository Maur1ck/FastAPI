from fastapi import APIRouter, HTTPException

from app.api.dependencies import DBDep, UserIdDep
from app.exceptions import ObjectNotFoundException
from app.schemas.bookings import BookingAddRequest, BookingAdd
from app.schemas.hotels import Hotel
from app.schemas.rooms import Room

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.post("")
async def add_booking(
    user_id: UserIdDep,
    db: DBDep,
    booking_data: BookingAddRequest,
):
    try:
        room: Room = await db.rooms.get_one(id=booking_data.room_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=400, detail="Номер не найден")
    hotel: Hotel = await db.hotels.get_one(id=room.hotel_id)
    room_price: int = room.price
    _booking_data = BookingAdd(
        user_id=user_id,
        price=room_price,
        **booking_data.model_dump(),
    )
    booking = await db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
    await db.commit()
    return {"status": "OK", "data": booking}


@router.get("")
async def get_bookings(db: DBDep):
    bookings = await db.bookings.get_all()
    return {"status": "OK", "data": bookings}


@router.get("/me")
async def get_me(user_id: UserIdDep, db: DBDep):
    bookings = await db.bookings.get_filtered(user_id=user_id)
    return {"status": "OK", "data": bookings}
