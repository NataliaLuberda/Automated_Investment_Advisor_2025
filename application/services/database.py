import os
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Generator

from dotenv import load_dotenv
from sqlalchemy import Table, MetaData, text
from sqlalchemy.orm import declarative_base

from config import DATABASE_URL

load_dotenv()

DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASS", "supersecurepassword")
DB_HOST = os.getenv("DB_HOST", "mysql")
DB_NAME = os.getenv("DB_NAME", "mydatabase")

DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class DatabaseError(Exception):
    """Base exception for database errors"""
    pass

class DatabaseConnectionError(DatabaseError):
    """Raised when there are connection issues"""
    pass

class DatabaseTransactionError(DatabaseError):
    """Raised when there are transaction issues"""
    pass

def init_db():
    """Initialize the database"""
    try:
        Base.metadata.create_all(bind=engine)
    except SQLAlchemyError as e:
        raise DatabaseConnectionError(f"Failed to initialize database: {str(e)}")

@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """Context manager for database sessions with proper error handling"""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        if isinstance(e, ConnectionError):
            raise DatabaseConnectionError(f"Database connection error: {str(e)}")
        raise DatabaseTransactionError(f"Database transaction error: {str(e)}")
    finally:
        session.close()

def get_db():
    """Get a database session"""
    db = SessionLocal()
    try:
        return db
    except SQLAlchemyError as e:
        raise DatabaseConnectionError(f"Failed to get database session: {str(e)}")
