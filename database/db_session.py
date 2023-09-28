# database/db_session.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models.base import Base

DATABASE_URL = "sqlite:///./test.db"  # Możesz dostosować URL do Twojej bazy danych

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
