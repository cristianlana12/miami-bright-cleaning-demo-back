from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers.bookings import router as bookings_router

app = FastAPI(title="Miami Bright Cleaning API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(bookings_router)


@app.get("/")
def health_check():
    return {"message": "Miami Bright Cleaning API is running"}