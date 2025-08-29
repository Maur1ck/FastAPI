import pytest


@pytest.mark.parametrize("email, password, status_code", [
    ("test@email.com", "test", 200),
    ("test@email.com", "test", 400),
    ("test1@email.com", "test1", 200),
    ("avcde", "1234", 422),
    ("awd@awd", "12345", 422),
])
async def test_auth_flow(email, password, status_code, ac):
    # /register
    response_register = await ac.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
        }
    )
    assert response_register.status_code == status_code
    if status_code != 200:
        return

    # /login
    response_login = await ac.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        }
    )
    assert response_login.status_code == status_code
    assert ac.cookies["access_token"] == response_login.json()["access_token"]

    # /me
    response_me = await ac.get("/auth/me")
    assert response_me.status_code == status_code
    assert response_me.json()["email"] == email

    # /logout
    response_logout = await ac.post("/auth/logout")
    assert response_logout.status_code == status_code
    assert "access_token" not in ac.cookies

    response_me2 = await ac.get("/auth/me")
    assert response_me2.status_code == 401
    assert response_me2.json()["detail"] == "Вы не предоставили токен"
