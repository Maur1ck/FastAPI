import pytest


@pytest.mark.parametrize("email, password, status_code", [
    ("test@email.com", "test", 200),
    ("test1@email.com", "test1", 200),
])
async def test_auth_flow(email, password, status_code, ac):
    response_register = await ac.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
        }
    )
    assert response_register.status_code == status_code

    response_login = await ac.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        }
    )
    assert response_login.status_code == status_code
    assert response_login.cookies["access_token"] == response_login.json()["access_token"]

    response_me = await ac.get("/auth/me")
    assert response_me.status_code == status_code
    assert response_me.json()["email"] == email

    response_logout = await ac.post("/auth/logout")
    assert response_logout.status_code == status_code
    assert response_logout.json()["message"] == "Logged out"

    response_me2 = await ac.get("/auth/me")
    assert response_me2.status_code == 401
    assert response_me2.json()["detail"] == "Вы не предоставили токен"
