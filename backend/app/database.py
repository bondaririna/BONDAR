import os
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine.url import make_url
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from app.config import get_settings

settings = get_settings()

_url = make_url(settings.database_url)
if _url.drivername == "sqlite" and _url.database and _url.database != ":memory:":
    _dir = os.path.dirname(os.path.abspath(_url.database))
    if _dir:
        os.makedirs(_dir, exist_ok=True)

connect_args = {"check_same_thread": False} if _url.drivername == "sqlite" else {}

engine = create_engine(
    settings.database_url,
    connect_args=connect_args,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
