from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import require_admin
from app.models import Event, EventStatus, User, UserRole
from app.schemas import EventRead, EventValidateBody, UserCreateStaff, UserPublic
from app.security import hash_password

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/organizers", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def create_organizer(
    body: UserCreateStaff,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
) -> User:
    if body.role != UserRole.ORGANIZER:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Rolul trebuie să fie organizer")
    email = body.email.strip().lower()
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Utilizator existent")
    user = User(
        email=email,
        full_name=body.full_name,
        role=UserRole.ORGANIZER,
        hashed_password=hash_password(body.password),
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.patch("/events/{event_id}/status", response_model=EventRead)
def set_event_status(
    event_id: int,
    body: EventValidateBody,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
) -> Event:
    ev = db.query(Event).filter(Event.id == event_id).first()
    if not ev:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Eveniment inexistent")
    if body.status not in (EventStatus.PUBLISHED, EventStatus.REJECTED):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="status trebuie să fie published sau rejected",
        )
    ev.status = body.status
    db.add(ev)
    db.commit()
    db.refresh(ev)
    return ev
