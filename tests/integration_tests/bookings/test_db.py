from datetime import date

from app.schemas.bookings import BookingAdd


async def test_booking_crud(db):
    user = (await db.users.get_all())[0]
    room = (await db.rooms.get_all())[0]
    booking_data = BookingAdd(
        date_from=date(year=2021, month=1, day=1),
        date_to=date(year=2021, month=1, day=15),
        room_id=room.id,
        user_id=user.id,
        price=100,
    )
    new_booking = await db.bookings.add(booking_data)

    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert booking
    assert booking.id == new_booking.id
    assert booking.room_id == room.id
    assert booking.user_id == user.id

    update_booking_data = BookingAdd(
        date_from=date(year=2021, month=1, day=1),
        date_to=date(year=2021, month=1, day=15),
        room_id=room.id,
        user_id=user.id,
        price=500,
    )
    await db.bookings.edit(data=update_booking_data, id=new_booking.id)
    updated_booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert updated_booking
    assert updated_booking.id == new_booking.id
    assert updated_booking.price == 500

    await db.bookings.delete(id=new_booking.id)
    booking_check = await db.bookings.get_one_or_none(id=new_booking.id)
    assert booking_check is None
