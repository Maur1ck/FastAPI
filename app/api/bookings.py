from fastapi import APIRouter

from app.api.dependencies import DBDep, UserIdDep
from app.schemas.bookings import BookingAdd, BookingAddRequest

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.post("")
async def create_booking(user_id: UserIdDep, booking_data: BookingAddRequest, db: DBDep):
    booking = await db.bookings.add_booking(user_id=user_id, booking_data=booking_data)
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
