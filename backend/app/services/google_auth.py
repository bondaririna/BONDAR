from google.auth.transport import requests
from google.oauth2 import id_token

from app.config import get_settings


class GoogleAuthError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


def verify_google_id_token(token: str) -> dict:
    settings = get_settings()
    if not settings.google_client_id:
        raise GoogleAuthError("GOOGLE_CLIENT_ID nu este configurat pe server")
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), settings.google_client_id)
    except ValueError as e:
        raise GoogleAuthError(f"Token Google invalid: {e}") from e
    return idinfo


def assert_student_usv_email(idinfo: dict) -> str:
    settings = get_settings()
    email = (idinfo.get("email") or "").strip().lower()
    suffix = settings.student_email_suffix.lower()
    if not email.endswith(suffix):
        raise GoogleAuthError(f"Doar conturi {suffix} sunt acceptate pentru studenți")
    if not idinfo.get("email_verified", False):
        raise GoogleAuthError("Adresa de email Google nu este verificată")
    return email


def get_google_subject(idinfo: dict) -> str:
    sub = idinfo.get("sub")
    if not sub:
        raise GoogleAuthError("Token Google fără identificator utilizator (sub)")
    return str(sub)
