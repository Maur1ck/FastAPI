async def test_get_facilities(ac):
    response = await ac.get("/facilities")
    assert response.status_code == 200


async def test_create_facility(ac):
    response = await ac.post(
        "/facilities",
        json={"title": "Test Facility"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "OK"
    assert response.json()["data"]["title"] == "Test Facility"
