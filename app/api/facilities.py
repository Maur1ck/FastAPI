import json

from fastapi import APIRouter, Body

from app.init import redis_manager
from app.schemas.facilities import FacilityAdd
from app.api.dependencies import DBDep

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
async def get_facilities(db: DBDep):
    facilities_from_cache = await redis_manager.get("facilities")
    if not facilities_from_cache:
        print("ИДУ В БД")
        facilities =  await db.facilities.get_all()
        facilities_schemas = [f.model_dump() for f in facilities]
        facilities_json = json.dumps(facilities_schemas)
        await redis_manager.set("facilities", facilities_json, 10)
        return facilities
    facilities_dict = json.loads(facilities_from_cache)
    return facilities_dict


@router.post("")
async def create_facility(db: DBDep, facility_data: FacilityAdd = Body()):
    facility = await db.facilities.add(facility_data)
    await db.commit()
    return {"status": "OK", "data": facility}
