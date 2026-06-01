from fastapi import APIRouter, HTTPException
from app.database import supabase
from app.schemas import BookingCreate, BookingStatusUpdate
from app.notifications import notify_customer

router = APIRouter(prefix="/bookings", tags=["bookings"])


ESTIMATED_PRICES = {
    "house_cleaning": 99,
    "deep_cleaning": 189,
    "office_cleaning": 149,
    "move_in_out": 229,
    "airbnb_cleaning": 129,
    "post_construction": 279,
}


@router.get("")
def list_bookings():
    response = (
        supabase
        .table("bookings")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )

    return response.data


@router.post("")
def create_booking(booking: BookingCreate):
    booking_data = booking.model_dump()

    booking_data["status"] = "pending"
    booking_data["estimated_price"] = ESTIMATED_PRICES[booking.service_type]

    response = (
        supabase
        .table("bookings")
        .insert(booking_data)
        .execute()
    )

    if not response.data:
        raise HTTPException(status_code=500, detail="Could not create booking")

    created_booking = response.data[0]

    try:
        notify_customer(created_booking, "pending")
    except Exception as error:
        print("Notification error:", error)

    return created_booking


@router.patch("/{booking_id}/status")
def update_booking_status(booking_id: str, payload: BookingStatusUpdate):
    current_response = (
        supabase
        .table("bookings")
        .select("*")
        .eq("id", booking_id)
        .single()
        .execute()
    )

    if not current_response.data:
        raise HTTPException(status_code=404, detail="Booking not found")

    update_response = (
        supabase
        .table("bookings")
        .update({"status": payload.status})
        .eq("id", booking_id)
        .execute()
    )

    if not update_response.data:
        raise HTTPException(status_code=500, detail="Could not update booking")

    updated_booking = update_response.data[0]

    try:
        notify_customer(updated_booking, payload.status)
    except Exception as error:
        print("Notification error:", error)

    return updated_booking