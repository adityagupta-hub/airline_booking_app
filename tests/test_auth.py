from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_register_and_login():
    email = "user_test@example.com"
    password = "StrongPass123!"

    register = client.post("/auth/register", json={"email": email, "password": password})
    assert register.status_code in (201, 409)

    login = client.post("/auth/login", json={"email": email, "password": password})
    assert login.status_code == 200
    body = login.json()
    assert "access_token" in body
