from app.models.rooms import RoomsORM
from app.repositories.base import BaseRepository


class RoomsRepository(BaseRepository):
    model = RoomsORM
