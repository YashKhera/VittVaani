from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}


def _normalize_database_url(url: str) -> str:
    # SQLAlchemy 2.0 maps a bare postgresql:// URL to the psycopg (v3) driver,
    # but this project ships psycopg2-binary. Pin the driver explicitly so the
    # app boots wherever a plain postgres URL is provided (Neon, Vercel, etc).
    # URLs that already name a driver (postgresql+...) are left untouched.
    if url.startswith("postgres://"):
        return "postgresql+psycopg2://" + url[len("postgres://"):]
    if url.startswith("postgresql://"):
        return "postgresql+psycopg2://" + url[len("postgresql://"):]
    return url

engine = create_engine(_normalize_database_url(settings.DATABASE_URL), connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()