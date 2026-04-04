from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models import User, UserRole
from app.schemas import GoogleAuthRequest, LoginRequest, TokenResponse, UserPublic
from app.security import create_access_token, verify_password
from app.services.google_auth import (
    GoogleAuthError,
    assert_student_usv_email,
    get_google_subject,
    verify_google_id_token,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/google", response_model=TokenResponse)
def auth_google(body: GoogleAuthRequest, db: Session = Depends(get_db)) -> TokenResponse:
    try:
        idinfo = verify_google_id_token(body.id_token)
        email = assert_student_usv_email(idinfo)
        sub = get_google_subject(idinfo)
    except GoogleAuthError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message) from e

    user = db.query(User).filter(User.google_sub == sub).first()
    if user:
        if user.email != email:
            user.email = email
            db.add(user)
            db.commit()
            db.refresh(user)
        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cont dezactivat")
        token = create_access_token(str(user.id), {"email": user.email, "role": user.role.value})
        return TokenResponse(access_token=token)

    existing = db.query(User).filter(User.email == email).first()
    if existing:
        if existing.role != UserRole.STUDENT:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acest email este înregistrat cu alt rol; folosiți autentificarea cu parolă",
            )
        if existing.google_sub and existing.google_sub != sub:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email asociat altui cont Google",
            )
        existing.google_sub = sub
        existing.full_name = existing.full_name or idinfo.get("name")
        db.add(existing)
        db.commit()
        db.refresh(existing)
        user = existing
    else:
        user = User(
            email=email,
            full_name=idinfo.get("name"),
            role=UserRole.STUDENT,
            google_sub=sub,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cont dezactivat")

    token = create_access_token(str(user.id), {"email": user.email, "role": user.role.value})
    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse)
def auth_login(body: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    email = body.username.strip().lower()
    user = db.query(User).filter(User.email == email).first()
    if not user or not user.hashed_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credențiale invalide")
    if user.role not in (UserRole.ORGANIZER, UserRole.ADMIN):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Autentificarea cu parolă este doar pentru organizatori și administratori",
        )
    if not verify_password(body.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credențiale invalide")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cont dezactivat")

    token = create_access_token(str(user.id), {"email": user.email, "role": user.role.value})
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserPublic)
def auth_me(user: User = Depends(get_current_user)) -> User:
    return user
