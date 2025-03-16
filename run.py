from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from application.database import DATABASE_URL
from application.main import start_app

if __name__ in {"__main__", "__mp_main__"}:
    Base = declarative_base()
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)
    start_app()
