from datetime import date

from fastapi import APIRouter, Query

from app.api.dependencies import DBDep
from app.schemas.facilities import RoomFacilityAdd
from app.schemas.rooms import RoomAdd, RoomPATCH, RoomAddRequest, RoomPatchRequest

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
        hotel_id: int,
        db: DBDep,
        date_from: date = Query(example="2025-08-01"),
        date_to: date = Query(example="2025-08-10"),
):
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    return await db.rooms.get_one_or_none(hotel_id=hotel_id, id=room_id)


@router.post("/{hotel_id}/rooms")
async def create_room(hotel_id: int, db: DBDep, room_data: RoomAddRequest):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)
    rooms_facilities_data = [RoomFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()
    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def change_room(
        hotel_id: int,
        room_id: int,
        db: DBDep,
        room_data: RoomAddRequest
):
    _room_data = RoomAddRequest(
        title=room_data.title,
        description=room_data.description,
        price=room_data.price,
        quantity=room_data.quantity,
    )
    await db.rooms.edit(_room_data, hotel_id=hotel_id, id=room_id, exclude_unset=True)

    facilities = await db.rooms_facilities.get_filtered(room_id=room_id)
    facilities_ids = [facility.model_dump().get("facility_id") for facility in facilities]

    facilities_for_delete = set(facilities_ids) - set(room_data.facilities_ids)
    if facilities_for_delete:
        for f_id in facilities_for_delete:
            await db.rooms_facilities.delete(room_id=room_id, facility_id=f_id)

    facilities_for_add = set(room_data.facilities_ids) - set(facilities_ids)
    if facilities_for_add:
        room_facilities_data_for_add = [RoomFacilityAdd(room_id=room_id, facility_id=f_id) for f_id in facilities_for_add]
        await db.rooms_facilities.add_bulk(room_facilities_data_for_add)

    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def changes_room(
        hotel_id: int,
        room_id: int,
        db: DBDep,
        room_data: RoomPatchRequest
):
    _room_data = RoomPATCH(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    await db.rooms.edit(_room_data, hotel_id=hotel_id, id=room_id, exclude_unset=True)

    if room_data.facilities_ids:
        facilities = await db.rooms_facilities.get_filtered(room_id=room_id)
        facilities_ids = [facility.model_dump().get("facility_id") for facility in facilities]

        facilities_for_delete = set(facilities_ids) - set(room_data.facilities_ids)
        if facilities_for_delete:
            for f_id in facilities_for_delete:
                await db.rooms_facilities.delete(room_id=room_id, facility_id=f_id)

        facilities_for_add = set(room_data.facilities_ids) - set(facilities_ids)
        if facilities_for_add:
            room_facilities_data_for_add = [RoomFacilityAdd(room_id=room_id, facility_id=f_id) for f_id in
                                            facilities_for_add]
            await db.rooms_facilities.add_bulk(room_facilities_data_for_add)

    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    await db.rooms.delete(hotel_id=hotel_id, id=room_id)
    await db.commit()
    return {"status": "OK"}
