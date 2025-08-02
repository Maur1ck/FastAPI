import pytest

from app.config import settings
from app.database import engine_null_pool, Base
from app.models import *


@pytest.fixture(scope="session", autouse=True)
async def async_main():
    print("ФИКСТУРА")
    assert settings.MODE == "TEST"

    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
