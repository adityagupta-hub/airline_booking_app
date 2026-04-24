from datetime import datetime, timedelta

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.config import get_settings
from app.database import Base, SessionLocal, engine
from app.models import Flight
from app.routers import auth, bookings, flights

settings = get_settings()
limiter = Limiter(key_func=get_remote_address, default_limits=[settings.rate_limit])

app = FastAPI(title=settings.app_name)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error."},
    )


@app.on_event("startup")
def startup() -> None:
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        has_flights = db.query(Flight).first()
        if not has_flights:
            now = datetime.utcnow()
            db.add_all(
                [
                    Flight(
                        flight_number="AB101",
                        origin="Delhi",
                        destination="Mumbai",
                        departure_time=now + timedelta(days=1),
                        base_price=4500.0,
                    ),
                    Flight(
                        flight_number="AB202",
                        origin="Bengaluru",
                        destination="Kolkata",
                        departure_time=now + timedelta(days=2),
                        base_price=5200.0,
                    ),
                ]
            )
            db.commit()
    finally:
        db.close()


@app.get("/health")
@limiter.limit(settings.rate_limit)
def health(request: Request):
    return {"status": "ok"}


app.include_router(auth.router)
app.include_router(flights.router)
app.include_router(bookings.router)
