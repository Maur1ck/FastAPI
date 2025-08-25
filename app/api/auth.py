from fastapi import APIRouter, HTTPException, Response

from app.api.dependencies import UserIdDep, DBDep
from app.schemas.users import UserRequestAdd, UserAdd
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])


@router.post("/register")
async def register_user(
        data: UserRequestAdd,
        db: DBDep,
):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    await db.users.add(new_user_data)
    await db.commit()

    return {"status": "OK"}


@router.post("/login")
async def login_user(
        data: UserRequestAdd,
        response: Response,
        db: DBDep,
):
    user = await db.users.get_user_with_hashed_password(email=data.email)
    await db.commit()
    if not user:
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")
    if not AuthService().verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Пароль не верный")
    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie(key="access_token", value=access_token)
    return {"access_token": access_token}


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out"}


@router.get("/me")
async def get_me(
        user_id: UserIdDep,
        db: DBDep,
):
    user = await db.users.get_one_or_none(id=user_id)
    return user
