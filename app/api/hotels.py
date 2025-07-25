from datetime import date

from fastapi import Query, APIRouter, Body
from fastapi.openapi.models import Example
from fastapi_cache.decorator import cache

from app.schemas.hotels import HotelAdd, HotelPATCH
from app.api.dependencies import PaginationDep, DBDep
from app.utils.decorators import cache_decorator

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
@cache_decorator(expire=15)
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        title: str | None = Query(None, description="Название отеля"),
        location: str | None = Query(None, description="Место"),
        date_from: date = Query(example="2025-08-01"),
        date_to: date = Query(example="2025-08-10"),
):
    per_page = pagination.per_page or 5
    print("ИДУ В БД")
    return await db.hotels.get_filtered_by_time(
        date_from=date_from,
        date_to=date_to,
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
