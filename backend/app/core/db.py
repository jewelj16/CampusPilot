import logging
from collections.abc import Generator
from functools import lru_cache

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session, sessionmaker, declarative_base

from app.core.config import get_settings

logger = logging.getLogger(__name__)

Base = declarative_base()

@lru_cache()
def get_engine() -> Engine:
    """
    Returns a singleton SQLAlchemy engine.
    We use lru_cache here to guarantee that the engine is created exactly once 
    per process, providing true connection pooling across the application.
    """
    settings = get_settings()
    db_url = settings.database_url
    if not db_url:
        raise ValueError("DATABASE_URL is not set in configuration")
    
    # create_engine already manages a connection pool internally
    engine = create_engine(db_url, pool_pre_ping=True)
    return engine


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that yields a database session for a single request.
    It guarantees the session is closed when the request finishes, and rolls back 
    the transaction if an exception occurs during request handling.
    """
    engine = get_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    session = SessionLocal()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
