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
    await db.bookings.add(booking_data)

    booking = await db.bookings.get_one_or_none(user_id=user.id, room_id=room.id)
    assert booking

    new_booking_data = BookingAdd(
        date_from=date(year=2021, month=1, day=1),
        date_to=date(year=2021, month=1, day=15),
        room_id=room.id,
        user_id=user.id,
        price=500,
    )
    await db.bookings.edit(data=new_booking_data, room_id=room.id, user_id=user.id)
    new_booking = await db.bookings.get_one_or_none(user_id=user.id, room_id=room.id)
    assert new_booking

    await db.bookings.delete(user_id=user.id, room_id=room.id)
    booking_check = await db.bookings.get_one_or_none(user_id=user.id, room_id=room.id)
    assert booking_check is None
