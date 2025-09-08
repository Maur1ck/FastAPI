from datetime import date

from fastapi import Query, APIRouter, Body
from fastapi.openapi.models import Example
from fastapi_cache.decorator import cache

from app.exceptions import HotelNotFoundHTTPException, ObjectNotFoundException
from app.schemas.hotels import HotelAdd, HotelPatch
from app.api.dependencies import PaginationDep, DBDep
from app.services.hotels import HotelService

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
@cache(expire=15)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description="Место"),
    date_from: date = Query(example="2025-08-01"),
    date_to: date = Query(example="2025-08-10"),
):
    return await HotelService(db).get_filtered_by_time(
        pagination,
        title,
        location,
        date_from,
        date_to
    )


@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int, db: DBDep):
    try:
        await HotelService(db).get_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


@router.post("")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": Example(
                summary="Сочи",
                value={"title": "Отель Сочи 5 звезд у моря", "location": "ул. Моря, 1"},
            ),
            "2": Example(
                summary="Дубай",
                value={"title": "Отель Дубай У фонтана", "location": "уд. Шейха, 2"},
            ),
        }
    ),
):
    hotel = HotelService(db).add_hotel(hotel_data)
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def change_hotel(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    await HotelService(db).edit_hotel(hotel_id, hotel_data)
    return {"status": "OK"}


@router.patch("/{hotel_id}")
async def changes_hotel(hotel_id: int, hotel_data: HotelPatch, db: DBDep):
    await HotelService(db).edit_hotel_partially(hotel_id, hotel_data, exclude_unset=True)
    return {"status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int, db: DBDep):
    await HotelService(db).hotel_delete(hotel_id)
    return {"status": "OK"}
