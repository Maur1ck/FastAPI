import json
import pytest
from httpx import AsyncClient

from app.api.dependencies import get_db
from app.config import settings
from app.database import engine_null_pool, Base, async_session_maker_null_pool
from app.main import app
from app.models import *
from app.schemas.hotels import HotelAdd
from app.schemas.rooms import RoomAdd
from app.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


async def get_db_null_pool():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


@pytest.fixture(scope="function")
async def db():
    async for db in get_db_null_pool():
        yield db


app.dependency_overrides[get_db] = get_db_null_pool


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    with open("tests/mock_hotels.json") as f:
        hotels_data = [HotelAdd.model_validate(item) for item in json.load(f)]
    with open("tests/mock_rooms.json") as f:
        rooms_data = [RoomAdd.model_validate(item) for item in json.load(f)]

    async with DBManager(session_factory=async_session_maker_null_pool) as db_:
        await db_.hotels.add_bulk(hotels_data)
        await db_.rooms.add_bulk(rooms_data)
        await db_.commit()


@pytest.fixture(scope="session")
async def ac():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def register_user(ac, setup_database):
    await ac.post(
        "/auth/register",
        json={
            "email": "kot@pes.com",
            "password": "123",
        }
    )
