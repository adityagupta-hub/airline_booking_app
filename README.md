# Airline Booking Ticket App (Secure FastAPI)

This project is a secure-by-default airline booking backend built with Python and FastAPI.

## Features

- User registration and login with hashed passwords (`bcrypt`)
- JWT-based authentication with expiry
- Flight listing endpoint
- Secure booking endpoints
- Seat double-booking prevention via DB unique constraint
- Rate limiting with `slowapi`
- Guardrails via `bandit` and `pip-audit`

## Setup

1. Create and activate virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Copy env template:

   ```bash
   copy .env.example .env
   ```

4. Run server:

   ```bash
   uvicorn app.main:app --reload
   ```

## API

- `POST /auth/register`
- `POST /auth/login`
- `GET /flights`
- `POST /bookings` (auth required)
- `GET /bookings/me` (auth required)
- `DELETE /bookings/{booking_id}` (auth required)

## Tests

```bash
pytest -q
```

## Security guardrail checks

```bash
bandit -r app
pip-audit
```
