from datetime import datetime, timezone, timedelta

from fastapi import APIRouter, HTTPException, Response

import jwt
from passlib.context import CryptContext

from app.database import async_session_maker
from app.repositories.users import UsersRepository
from app.schemas.users import UserRequestAdd, UserAdd

router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode |= {"exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/register")
async def register_user(
        data: UserRequestAdd
):
    hashed_password = pwd_context.hash(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        user = await UsersRepository(session).add(new_user_data)
        await session.commit()
    if user["status"]:
        return user
    return {"status": "OK"}


@router.post("/login")
async def register_user(
        data: UserRequestAdd,
        response: Response
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(email=data.email)
        await session.commit()
        if not user:
            raise HTTPException(status_code=401, detail="Неверный логин или пароль")
        if not verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Пароль не верный")
        access_token = create_access_token({"user_id": user.id})
        response.set_cookie(key="access_token", value=access_token)
        return {"access_token": access_token}
