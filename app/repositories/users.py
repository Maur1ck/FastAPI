from app.models.users import UsersORM
from app.repositories.base import BaseRepository
from app.schemas.users import User


class UsersRepository(BaseRepository):
    model = UsersORM
    schema = User
