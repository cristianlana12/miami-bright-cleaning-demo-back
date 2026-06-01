# backend/app/config.py

from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseModel):
    supabase_url: str = os.getenv("SUPABASE_URL", "")
    supabase_service_role_key: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")

    frontend_url: str = os.getenv("FRONTEND_URL", "http://localhost:5173")

    smtp_host: str = os.getenv("SMTP_HOST", "")
    smtp_port: int = int(os.getenv("SMTP_PORT", "587"))
    smtp_user: str = os.getenv("SMTP_USER", "")
    smtp_password: str = os.getenv("SMTP_PASSWORD", "")
    smtp_from: str = os.getenv("SMTP_FROM", "")

    whatsapp_enabled: bool = os.getenv("WHATSAPP_ENABLED", "false").lower() == "true"
    whatsapp_api_url: str = os.getenv("WHATSAPP_API_URL", "")
    whatsapp_token: str = os.getenv("WHATSAPP_TOKEN", "")
    whatsapp_from_phone_id: str = os.getenv("WHATSAPP_FROM_PHONE_ID", "")


settings = Settings()