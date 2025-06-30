from sqlalchemy import insert, select

from app.models.rooms import RoomsORM
from app.repositories.base import BaseRepository
from app.schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsORM
    schema = Room
