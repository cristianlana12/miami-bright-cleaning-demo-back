# backend/app/schemas.py

from pydantic import BaseModel, EmailStr
from typing import Optional, Literal


ServiceType = Literal[
    "house_cleaning",
    "deep_cleaning",
    "office_cleaning",
    "move_in_out",
    "airbnb_cleaning",
    "post_construction",
]

BookingStatus = Literal[
    "pending",
    "confirmed",
    "completed",
    "cancelled",
]


class BookingCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    service_type: ServiceType
    booking_date: str
    booking_time: str
    address: str
    message: Optional[str] = None


class BookingStatusUpdate(BaseModel):
    status: BookingStatus