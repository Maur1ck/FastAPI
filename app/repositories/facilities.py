from app.models.facilities import FacilitiesOrm
from app.repositories.base import BaseRepository
from app.schemas.facitilies import Facility


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facility
