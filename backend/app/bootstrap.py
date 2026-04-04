from sqlalchemy.orm import Session

from app.config import get_settings
from app.models import User, UserRole
from app.security import hash_password


def ensure_bootstrap_admin(db: Session) -> None:
    settings = get_settings()
    pwd = settings.bootstrap_admin_password.strip()
    if not pwd:
        return
    email = settings.bootstrap_admin_email.strip().lower()
    if db.query(User).filter(User.email == email).first():
        return
    admin = User(
        email=email,
        full_name="Administrator",
        role=UserRole.ADMIN,
        hashed_password=hash_password(pwd),
        is_active=True,
    )
    db.add(admin)
    db.commit()
