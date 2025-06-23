from fastapi import APIRouter

from app.database import async_session_maker
from app.models.rooms import RoomsORM
from app.repositories.users import UsersRepository
from app.schemas.users import UserRequestAdd, UserAdd

router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])


@router.post("/register")
async def register_user(
        data: UserRequestAdd
):
    hashed_password = data.hashed_password
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        user = await UsersRepository(session).add(new_user_data)
        await session.commit()

    return {"status": "OK"}