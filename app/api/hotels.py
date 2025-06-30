from fastapi import Query, APIRouter, Body
from fastapi.openapi.models import Example

from app.database import async_session_maker
from app.repositories.hotels import HotelsRepository
from app.schemas.hotels import HotelAdd, HotelPATCH
from app.api.dependencies import PaginationDep, DBDep

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
async def get_hotels(pagination: PaginationDep,
                     db: DBDep,
                     title: str | None = Query(None, description="Название отеля"),
                     location: str | None = Query(None, description="Место")):
    per_page = pagination.per_page or 5
    return await db.hotels.get_all(
        location=location,
        title=title,
        limit=per_page,
        offset=per_page * (pagination.page - 1),
    )


@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int, db: DBDep):
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.post("")
async def create_hotel(
        db: DBDep,
        hotel_data: HotelAdd = Body(openapi_examples={
    "1": Example(
        summary="Сочи",
        value={"title": "Отель Сочи 5 звезд у моря", "location": "ул. Моря, 1"}
    ),
    "2": Example(
        summary="Дубай",
        value={"title": "Отель Дубай У фонтана", "location": "уд. Шейха, 2"}
    ),
})):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()

    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def change_hotel(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}")
async def changes_hotel(hotel_id: int, hotel_data: HotelPATCH, db: DBDep):
    await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int, db: DBDep):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "OK"}
