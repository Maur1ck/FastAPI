from fastapi import APIRouter

from app.api.dependencies import DBDep
from app.schemas.rooms import RoomAdd, RoomPATCH, RoomAddRequest

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int, db: DBDep):
    return await db.rooms.get_filtered(hotel_id=hotel_id)


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    return await db.rooms.get_one_or_none(hotel_id=hotel_id, id=room_id)


@router.post("/{hotel_id}/rooms")
async def create_room(hotel_id: int, db: DBDep, room_data: RoomAddRequest):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)
    await db.commit()
    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def change_room(
        hotel_id: int,
        room_id: int,
        db: DBDep,
        room_data: RoomAddRequest
):
    await db.rooms.edit(room_data, hotel_id=hotel_id, id=room_id)
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def changes_room(
        hotel_id: int,
        room_id: int,
        db: DBDep,
        room_data: RoomPATCH
):
    await db.rooms.edit(room_data, hotel_id=hotel_id, id=room_id, exclude_unset=True)
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    await db.rooms.delete(hotel_id=hotel_id, id=room_id)
    await db.commit()
    return {"status": "OK"}
