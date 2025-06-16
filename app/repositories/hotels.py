from app.models.hotels import HotelsORM
from app.repositories.base import BaseRepository


class HotelsRepository(BaseRepository):
    model = HotelsORM
