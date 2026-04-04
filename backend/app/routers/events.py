from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user_optional, require_staff, require_student
from app.models import Event, EventCategory, EventFeedback, EventStatus, ParticipationMode, User, UserRole
from app.schemas import EventCreate, EventRead, EventUpdate, FeedbackCreate, FeedbackRead

router = APIRouter(prefix="/events", tags=["events"])


@router.get("", response_model=list[EventRead])
def list_events(
    db: Session = Depends(get_db),
    user: User | None = Depends(get_current_user_optional),
    faculty_or_department: str | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    category: EventCategory | None = None,
    location: str | None = None,
    organizer_name: str | None = None,
    participation_mode: ParticipationMode | None = None,
    free_entry: bool | None = None,
    requires_registration: bool | None = None,
    has_qr: bool | None = None,
    q: str | None = None,
) -> list[Event]:
    qry = db.query(Event)

    if user is None or user.role == UserRole.STUDENT:
        qry = qry.filter(Event.status == EventStatus.PUBLISHED)
    elif user.role == UserRole.ORGANIZER:
        qry = qry.filter(
            or_(Event.status == EventStatus.PUBLISHED, Event.organizer_user_id == user.id)
        )
    # admin: no status filter

    if faculty_or_department:
        qry = qry.filter(Event.faculty_or_department.ilike(f"%{faculty_or_department}%"))
    if date_from:
        qry = qry.filter(Event.start_at >= date_from)
    if date_to:
        qry = qry.filter(Event.start_at <= date_to)
    if category:
        qry = qry.filter(Event.category == category)
    if location:
        qry = qry.filter(Event.location.ilike(f"%{location}%"))
    if organizer_name:
        qry = qry.filter(Event.organizer_name.ilike(f"%{organizer_name}%"))
    if participation_mode:
        qry = qry.filter(Event.participation_mode == participation_mode)
    if free_entry is not None:
        qry = qry.filter(Event.free_entry == free_entry)
    if requires_registration is not None:
        qry = qry.filter(Event.requires_registration == requires_registration)
    if has_qr is not None:
        if has_qr:
            qry = qry.filter(Event.qr_payload.isnot(None), Event.qr_payload != "")
        else:
            qry = qry.filter(or_(Event.qr_payload.is_(None), Event.qr_payload == ""))
    if q:
        like = f"%{q}%"
        qry = qry.filter(or_(Event.title.ilike(like), Event.description.ilike(like)))

    rows = qry.order_by(Event.start_at.asc()).all()
    return rows


@router.get("/{event_id}", response_model=EventRead)
def get_event(
    event_id: int,
    db: Session = Depends(get_db),
    user: User | None = Depends(get_current_user_optional),
) -> Event:
    ev = db.query(Event).filter(Event.id == event_id).first()
    if not ev:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Eveniment inexistent")

    if ev.status == EventStatus.PUBLISHED:
        return ev
    if user and user.role == UserRole.ADMIN:
        return ev
    if user and user.role == UserRole.ORGANIZER and ev.organizer_user_id == user.id:
        return ev
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Eveniment inexistent")


@router.post("", response_model=EventRead, status_code=status.HTTP_201_CREATED)
def create_event(
    body: EventCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_staff),
) -> Event:
    st = body.status
    if user.role == UserRole.ORGANIZER:
        st = EventStatus.PENDING if st is None else st
        if st not in (EventStatus.DRAFT, EventStatus.PENDING):
            st = EventStatus.PENDING
    elif user.role == UserRole.ADMIN:
        st = st or EventStatus.PUBLISHED

    ev = Event(
        title=body.title,
        description=body.description,
        start_at=body.start_at,
        end_at=body.end_at,
        location=body.location,
        faculty_or_department=body.faculty_or_department,
        category=body.category,
        participation_mode=body.participation_mode,
        organizer_name=body.organizer_name or (user.full_name or user.email),
        organizer_user_id=user.id,
        registration_link=body.registration_link,
        qr_payload=body.qr_payload,
        sponsors_json=body.sponsors_json,
        requires_registration=body.requires_registration,
        free_entry=body.free_entry,
        status=st,
    )
    db.add(ev)
    db.commit()
    db.refresh(ev)
    return ev


@router.patch("/{event_id}", response_model=EventRead)
def update_event(
    event_id: int,
    body: EventUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(require_staff),
) -> Event:
    ev = db.query(Event).filter(Event.id == event_id).first()
    if not ev:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Eveniment inexistent")
    if user.role == UserRole.ORGANIZER and ev.organizer_user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Nu puteți edita acest eveniment")

    data = body.model_dump(exclude_unset=True)
    if user.role == UserRole.ORGANIZER and "status" in data:
        if data["status"] not in (EventStatus.DRAFT, EventStatus.PENDING, None):
            del data["status"]
    for k, v in data.items():
        setattr(ev, k, v)
    db.add(ev)
    db.commit()
    db.refresh(ev)
    return ev


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(
    event_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_staff),
) -> None:
    ev = db.query(Event).filter(Event.id == event_id).first()
    if not ev:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Eveniment inexistent")
    if user.role == UserRole.ORGANIZER and ev.organizer_user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Nu puteți șterge acest eveniment")
    db.delete(ev)
    db.commit()


@router.post("/{event_id}/feedback", response_model=FeedbackRead, status_code=status.HTTP_201_CREATED)
def add_feedback(
    event_id: int,
    body: FeedbackCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_student),
) -> EventFeedback:
    ev = db.query(Event).filter(Event.id == event_id).first()
    if not ev or ev.status != EventStatus.PUBLISHED:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Eveniment inexistent")
    now = datetime.utcnow()
    if now < ev.end_at:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Feedback disponibil după încheierea evenimentului",
        )
    existing = (
        db.query(EventFeedback)
        .filter(EventFeedback.event_id == event_id, EventFeedback.user_id == user.id)
        .first()
    )
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ați trimis deja feedback pentru acest eveniment")

    fb = EventFeedback(event_id=event_id, user_id=user.id, rating=body.rating, comment=body.comment)
    db.add(fb)
    db.commit()
    db.refresh(fb)
    return fb
