from sqlalchemy import select, delete, insert

from app.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from app.repositories.base import BaseRepository
from app.repositories.mappers.mappers import FacilityDataMapper, RoomFacilityDataMapper


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    mapper = FacilityDataMapper


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    mapper = RoomFacilityDataMapper

    async def set_room_facilities(self, room_id: int, facilities_ids: list[int]):
        query = select(self.model.facility_id).filter_by(room_id=room_id)
        res = await self.session.execute(query)
        current_facilities_ids = res.scalars().all()
        ids_to_delete = list(set(current_facilities_ids) - set(facilities_ids))
        ids_to_add = list(set(facilities_ids) - set(current_facilities_ids))

        if ids_to_delete:
            delete_m2m_facilities_stmt = delete(self.model).filter(
                self.model.room_id == room_id,
                self.model.facility_id.in_(ids_to_delete)
            )
            await self.session.execute(delete_m2m_facilities_stmt)

        if ids_to_add:
            insert_m2m_facilities_stmt = (
                insert(self.model)
                .values([{"room_id": room_id, "facility_id": f_id} for f_id in ids_to_add])
            )
            await self.session.execute(insert_m2m_facilities_stmt)
