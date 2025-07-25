from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from app.schemas.facilities import FacilityAdd
from app.api.dependencies import DBDep
from app.utils.decorators import cache_decorator

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
@cache_decorator(expire=15)
async def get_facilities(db: DBDep):
    print("Иду в бд")
    return await db.facilities.get_all()


@router.post("")
async def create_facility(db: DBDep, facility_data: FacilityAdd = Body()):
    facility = await db.facilities.add(facility_data)
    await db.commit()
    return {"status": "OK", "data": facility}
