import enum
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum as SQLEnum, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def _enum_values(enum_cls: type[enum.Enum]) -> list[str]:
    return [m.value for m in enum_cls]


class UserRole(str, enum.Enum):
    STUDENT = "student"
    ORGANIZER = "organizer"
    ADMIN = "admin"


class EventCategory(str, enum.Enum):
    ACADEMIC = "academic"
    SPORT = "sport"
    CAREER = "career"
    VOLUNTEERING = "volunteering"
    CULTURAL = "cultural"
    OTHER = "other"


class ParticipationMode(str, enum.Enum):
    PHYSICAL = "physical"
    ONLINE = "online"
    HYBRID = "hybrid"


class EventStatus(str, enum.Enum):
    DRAFT = "draft"
    PENDING = "pending"
    PUBLISHED = "published"
    REJECTED = "rejected"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str | None] = mapped_column(String(255), nullable=True)
    full_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    role: Mapped[UserRole] = mapped_column(
        SQLEnum(UserRole, native_enum=False, values_callable=_enum_values), nullable=False, default=UserRole.STUDENT
    )
    google_sub: Mapped[str | None] = mapped_column(String(255), unique=True, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    events_organized: Mapped[list["Event"]] = relationship(
        "Event", back_populates="organizer_user", foreign_keys="Event.organizer_user_id"
    )
    feedbacks: Mapped[list["EventFeedback"]] = relationship("EventFeedback", back_populates="user")


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    start_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    end_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    location: Mapped[str] = mapped_column(String(500), default="")
    faculty_or_department: Mapped[str] = mapped_column(String(500), default="")
    category: Mapped[EventCategory] = mapped_column(
        SQLEnum(EventCategory, native_enum=False, values_callable=_enum_values), nullable=False
    )
    participation_mode: Mapped[ParticipationMode] = mapped_column(
        SQLEnum(ParticipationMode, native_enum=False, values_callable=_enum_values), nullable=False
    )
    organizer_name: Mapped[str] = mapped_column(String(500), default="")
    organizer_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    registration_link: Mapped[str | None] = mapped_column(String(2000), nullable=True)
    qr_payload: Mapped[str | None] = mapped_column(String(2000), nullable=True)
    sponsors_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    requires_registration: Mapped[bool] = mapped_column(Boolean, default=False)
    free_entry: Mapped[bool] = mapped_column(Boolean, default=True)
    status: Mapped[EventStatus] = mapped_column(
        SQLEnum(EventStatus, native_enum=False, values_callable=_enum_values),
        nullable=False,
        default=EventStatus.PENDING,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    organizer_user: Mapped["User | None"] = relationship(
        "User", back_populates="events_organized", foreign_keys=[organizer_user_id]
    )
    feedbacks: Mapped[list["EventFeedback"]] = relationship("EventFeedback", back_populates="event")


class EventFeedback(Base):
    __tablename__ = "event_feedback"
    __table_args__ = (UniqueConstraint("event_id", "user_id", name="uq_feedback_event_user"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    event: Mapped["Event"] = relationship("Event", back_populates="feedbacks")
    user: Mapped["User"] = relationship("User", back_populates="feedbacks")
