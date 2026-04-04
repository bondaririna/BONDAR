from collections.abc import Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, UserRole
from app.security import safe_decode_token

security = HTTPBearer(auto_error=False)


def _user_from_payload(db: Session, payload: dict) -> User | None:
    sub = payload.get("sub")
    if not sub:
        return None
    try:
        user_id = int(sub)
    except (TypeError, ValueError):
        return None
    return db.query(User).filter(User.id == user_id).first()


def get_current_user_optional(
    cred: HTTPAuthorizationCredentials | None = Depends(security),
    db: Session = Depends(get_db),
) -> User | None:
    if not cred or cred.scheme.lower() != "bearer":
        return None
    payload = safe_decode_token(cred.credentials)
    if not payload:
        return None
    user = _user_from_payload(db, payload)
    if not user or not user.is_active:
        return None
    return user


def get_current_user(
    user: User | None = Depends(get_current_user_optional),
) -> User:
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Autentificare necesară",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def require_roles(*roles: UserRole) -> Callable[[User], User]:
    allowed = set(roles)

    def _dep(user: User = Depends(get_current_user)) -> User:
        if user.role not in allowed:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permisiuni insuficiente")
        return user

    return _dep


require_student = require_roles(UserRole.STUDENT)
require_organizer = require_roles(UserRole.ORGANIZER)
require_admin = require_roles(UserRole.ADMIN)
require_staff = require_roles(UserRole.ORGANIZER, UserRole.ADMIN)
