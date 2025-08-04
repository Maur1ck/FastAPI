from datetime import date

from app.schemas.bookings import BookingAdd


async def test_add_booking(db):
    user = (await db.users.get_all())[0]
    room = (await db.rooms.get_all())[0]
    booking_data = BookingAdd(
        date_from=date(year=2021, month=1, day=1),
        date_to=date(year=2021, month=1, day=15),
        room_id=room.id,
        user_id=user.id,
        price=100,
    )
    await db.bookings.add(booking_data)
    await db.commit()
