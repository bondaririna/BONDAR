from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator

from app.models import EventCategory, EventStatus, ParticipationMode, UserRole


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class GoogleAuthRequest(BaseModel):
    id_token: str = Field(..., min_length=10, description="Google ID token (JWT) from client Sign-In")


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1, description="Email sau nume utilizator")
    password: str = Field(..., min_length=1)


class UserPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    full_name: str | None
    role: UserRole
    is_active: bool


class UserCreateStaff(BaseModel):
    """Creare organizator de către admin (parolă inițială)."""

    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: str | None = None
    role: UserRole = UserRole.ORGANIZER


class EventBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    description: str = ""
    start_at: datetime
    end_at: datetime
    location: str = ""
    faculty_or_department: str = ""
    category: EventCategory
    participation_mode: ParticipationMode
    organizer_name: str = ""
    registration_link: str | None = None
    qr_payload: str | None = None
    sponsors_json: str | None = None
    requires_registration: bool = False
    free_entry: bool = True

    @model_validator(mode="after")
    def end_after_start(self) -> "EventBase":
        if self.end_at < self.start_at:
            raise ValueError("end_at trebuie să fie după sau la start_at")
        return self


class EventCreate(EventBase):
    status: EventStatus | None = None


class EventUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=500)
    description: str | None = None
    start_at: datetime | None = None
    end_at: datetime | None = None
    location: str | None = None
    faculty_or_department: str | None = None
    category: EventCategory | None = None
    participation_mode: ParticipationMode | None = None
    organizer_name: str | None = None
    registration_link: str | None = None
    qr_payload: str | None = None
    sponsors_json: str | None = None
    requires_registration: bool | None = None
    free_entry: bool | None = None
    status: EventStatus | None = None


class EventRead(EventBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    organizer_user_id: int | None
    status: EventStatus
    created_at: datetime
    updated_at: datetime


class EventListFilters(BaseModel):
    faculty_or_department: str | None = None
    date_from: datetime | None = None
    date_to: datetime | None = None
    category: EventCategory | None = None
    location: str | None = None
    organizer_name: str | None = None
    participation_mode: ParticipationMode | None = None
    free_entry: bool | None = None
    requires_registration: bool | None = None
    has_qr: bool | None = None
    q: str | None = Field(None, description="Căutare text în titlu/descriere")


class FeedbackCreate(BaseModel):
    rating: float = Field(..., ge=1, le=5)
    comment: str | None = Field(None, max_length=5000)


class FeedbackRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    event_id: int
    user_id: int
    rating: float
    comment: str | None
    created_at: datetime


class EventValidateBody(BaseModel):
    status: EventStatus = Field(..., description="published sau rejected")
