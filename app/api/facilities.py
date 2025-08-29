from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from app.schemas.facilities import FacilityAdd
from app.api.dependencies import DBDep
from app.tasks.tasks import test_task

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
@cache(expire=15)
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()


@router.post("")
async def create_facility(db: DBDep, facility_data: FacilityAdd = Body()):
    facility = await db.facilities.add(facility_data)
    await db.commit()

    test_task.delay() # type: ignore

    return {"status": "OK", "data": facility}
