from fastapi import Query, APIRouter, Body
from fastapi.openapi.models import Example
from sqlalchemy import insert, select

from app.database import async_session_maker
from app.models.hotels import HotelsORM
from app.schemas.hotels import Hotel, HotelPATCH
from app.api.dependencies import PaginationDep

router = APIRouter(prefix="/routers", tags=["Отели"])


@router.get("")
async def get_hotels(pagination: PaginationDep,
                     title: str | None = Query(None, description="Название отеля"),
                     location: str | None = Query(None, description="Место")):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        query = select(HotelsORM)
        if title:
            query = query.where(HotelsORM.title.like(f"%{title}%"))
        if location:
            query = query.where(HotelsORM.location.like(f"%{location}%"))
        query = (
            query
            .limit(per_page)
            .offset((pagination.page - 1) * per_page)
        )
        result = await session.execute(query)
        hotels = result.scalars().all()
        return hotels


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
        add_hotel_stmt = insert(HotelsORM).values(**hotel_data.model_dump())
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {"status": "OK"}


@router.put("/{hotel_id}")
def change_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_data.title
            hotel["name"] = hotel_data.name
            break
    return {"status": "OK"}


@router.patch("/{hotel_id}")
def changes_hotel(hotel_id: int, hotel_data: HotelPATCH):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_data.title:
                hotel["title"] = hotel_data.title
            if hotel_data.name:
                hotel["name"] = hotel_data.name
            break
    return {"status": "OK"}


@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}
