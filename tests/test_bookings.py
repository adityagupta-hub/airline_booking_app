from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def _get_token(email: str, password: str) -> str:
    client.post("/auth/register", json={"email": email, "password": password})
    login = client.post("/auth/login", json={"email": email, "password": password})
    return login.json()["access_token"]


def test_create_booking_and_list_my_bookings():
    token = _get_token("booking_test@example.com", "StrongPass123!")
    flights = client.get("/flights")
    assert flights.status_code == 200
    flight_id = flights.json()[0]["id"]

    book = client.post(
        "/bookings",
        json={"flight_id": flight_id, "seat_number": "12A"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert book.status_code in (201, 409)

    my_bookings = client.get("/bookings/me", headers={"Authorization": f"Bearer {token}"})
    assert my_bookings.status_code == 200
