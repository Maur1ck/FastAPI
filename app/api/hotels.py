from fastapi import Query, APIRouter, Body
from fastapi.openapi.models import Example

from app.database import async_session_maker
from app.repositories.hotels import HotelsRepository
from app.schemas.hotels import Hotel, HotelPATCH
from app.api.dependencies import PaginationDep

router = APIRouter(prefix="/routers", tags=["Отели"])


@router.get("")
async def get_hotels(pagination: PaginationDep,
                     title: str | None = Query(None, description="Название отеля"),
                     location: str | None = Query(None, description="Место")):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
        )


@router.post("")
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": Example(
        summary="Сочи",
        value={"title": "Отель Сочи 5 звезд у моря", "location": "ул. Моря, 1"}
    ),
    "2": Example(
        summary="Дубай",
        value={"title": "Отель Дубай У фонтана", "location": "уд. Шейха, 2"}
    ),
})):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def change_hotel(hotel_id: int, hotel_data: Hotel):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}")
async def changes_hotel(hotel_id: int, hotel_data: HotelPATCH):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, exclude_unset=True, id=hotel_id)
    return {"status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {"status": "OK"}
