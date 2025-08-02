import json
import pytest
from httpx import AsyncClient

from app.config import settings
from app.database import engine_null_pool, Base, async_session_maker_null_poll
from app.main import app
from app.models import *
from app.schemas.hotels import HotelAdd
from app.schemas.rooms import RoomAdd
from app.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    with open("tests/mock_hotels.json") as f:
        hotels_data = [HotelAdd.model_validate(item) for item in json.load(f)]
    with open("tests/mock_rooms.json") as f:
        rooms_data = [RoomAdd.model_validate(item) for item in json.load(f)]

    async with DBManager(session_factory=async_session_maker_null_poll) as db:
        await db.hotels.add_bulk(hotels_data)
        await db.rooms.add_bulk(rooms_data)
        await db.commit()


@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_database):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post(
            "/auth/register",
            json={
                "email": "kot@pes.com",
                "password": "123",
            }
        )
