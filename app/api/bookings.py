from fastapi import APIRouter

from app.api.dependencies import DBDep, UserIdDep
from app.exceptions import AllRoomsAreBookedException, AllRoomsAreBookedHTTPException, RoomNotFoundException, \
    RoomNotFoundHTTPException
from app.schemas.bookings import BookingAddRequest
from app.services.bookings import BookingService

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.post("")
async def add_booking(
    user_id: UserIdDep,
    db: DBDep,
    booking_data: BookingAddRequest,
):
    try:
        booking = await BookingService(db).add_booking(user_id, booking_data)
    except AllRoomsAreBookedException:
        raise AllRoomsAreBookedHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    return {"status": "OK", "data": booking}


@router.get("")
async def get_bookings(db: DBDep):
    return await BookingService(db).get_bookings()


@router.get("/me")
async def get_me(user_id: UserIdDep, db: DBDep):
    return await BookingService(db).get_my_bookings(user_id)
