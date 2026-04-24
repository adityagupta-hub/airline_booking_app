from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=12, max_length=128)

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, value: str) -> str:
        if not any(c.isupper() for c in value):
            raise ValueError("Password must include at least one uppercase letter.")
        if not any(c.islower() for c in value):
            raise ValueError("Password must include at least one lowercase letter.")
        if not any(c.isdigit() for c in value):
            raise ValueError("Password must include at least one digit.")
        if not any(not c.isalnum() for c in value):
            raise ValueError("Password must include at least one special character.")
        return value


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True


class FlightOut(BaseModel):
    id: int
    flight_number: str
    origin: str
    destination: str
    departure_time: datetime
    base_price: float

    class Config:
        from_attributes = True


class BookingCreate(BaseModel):
    flight_id: int = Field(gt=0)
    seat_number: str = Field(pattern=r"^\d{1,2}[A-F]$")


class BookingOut(BaseModel):
    id: int
    flight_id: int
    seat_number: str
    price_paid: float
    created_at: datetime

    class Config:
        from_attributes = True
