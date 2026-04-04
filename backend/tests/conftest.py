import os

# Must run before importing the application package
os.environ.setdefault("DATABASE_URL", "sqlite:///./test_data.db")
os.environ.setdefault("JWT_SECRET", "test-secret-key-for-pytest-only")
os.environ.setdefault("GOOGLE_CLIENT_ID", "test.apps.googleusercontent.com")
os.environ.setdefault("BOOTSTRAP_ADMIN_PASSWORD", "")
os.environ.setdefault("BOOTSTRAP_ADMIN_EMAIL", "admin@test.local")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.database import Base, SessionLocal, engine
from app.main import app
from app.models import User, UserRole
from app.security import create_access_token, hash_password


@pytest.fixture(autouse=True)
def reset_database() -> None:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client() -> TestClient:
    with TestClient(app) as c:
        yield c


@pytest.fixture()
def db_session() -> Session:
    s = SessionLocal()
    try:
        yield s
    finally:
        s.close()


@pytest.fixture()
def admin_user(db_session: Session) -> User:
    u = User(
        email="admin@test.local",
        full_name="Admin",
        role=UserRole.ADMIN,
        hashed_password=hash_password("adminpass123"),
        is_active=True,
    )
    db_session.add(u)
    db_session.commit()
    db_session.refresh(u)
    return u


@pytest.fixture()
def admin_token(admin_user: User) -> str:
    return create_access_token(str(admin_user.id), {"email": admin_user.email, "role": admin_user.role.value})


@pytest.fixture()
def organizer_user(db_session: Session) -> User:
    u = User(
        email="org@test.local",
        full_name="Org",
        role=UserRole.ORGANIZER,
        hashed_password=hash_password("orgpass123"),
        is_active=True,
    )
    db_session.add(u)
    db_session.commit()
    db_session.refresh(u)
    return u


@pytest.fixture()
def organizer_token(organizer_user: User) -> str:
    return create_access_token(
        str(organizer_user.id), {"email": organizer_user.email, "role": organizer_user.role.value}
    )


@pytest.fixture()
def student_user(db_session: Session) -> User:
    u = User(
        email="student@student.usv.ro",
        full_name="Student",
        role=UserRole.STUDENT,
        google_sub="google-sub-1",
        is_active=True,
    )
    db_session.add(u)
    db_session.commit()
    db_session.refresh(u)
    return u


@pytest.fixture()
def student_token(student_user: User) -> str:
    return create_access_token(
        str(student_user.id), {"email": student_user.email, "role": student_user.role.value}
    )


