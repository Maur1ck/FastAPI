import pytest

from tests.conftest import get_db_null_pool


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code",
    [
        (1, "2021-05-01", "2021-05-10", 200),
        (1, "2021-05-02", "2021-05-11", 200),
        (1, "2021-05-03", "2021-05-12", 200),
        (1, "2021-05-04", "2021-05-13", 200),
        (1, "2021-05-05", "2021-05-14", 200),
        (1, "2021-05-06", "2021-05-15", 404),
        (1, "2021-05-17", "2021-05-25", 200),
    ],
)
async def test_add_booking(room_id, date_from, date_to, status_code, db, authenticated_ac):
    # room_id = (await db.rooms.get_all())[0].id
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert res["status"] == "OK"
        assert "data" in res


@pytest.fixture(scope="module")
async def delete_all_bookings():
    async for _db in get_db_null_pool():
        await _db.bookings.delete()
        await _db.commit()


@pytest.mark.parametrize(
    "room_id, date_from, date_to, quantity",
    [
        (1, "2021-05-01", "2021-05-10", 1),
        (1, "2021-05-02", "2021-05-11", 2),
        (1, "2021-05-03", "2021-05-12", 3),
    ],
)
async def test_add_and_get_bookings(
    room_id, date_from, date_to, quantity, authenticated_ac, delete_all_bookings
):
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    assert response.status_code == 200

    response2 = await authenticated_ac.get("/bookings/me")
    assert response2.status_code == 200
    res = response2.json()
    assert len(res["data"]) == quantity
