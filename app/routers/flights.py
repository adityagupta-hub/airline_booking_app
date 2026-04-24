from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Flight
from app.schemas import FlightOut

router = APIRouter(prefix="/flights", tags=["flights"])


@router.get("", response_model=list[FlightOut])
def list_flights(db: Session = Depends(get_db)):
    return db.query(Flight).order_by(Flight.departure_time.asc()).all()
