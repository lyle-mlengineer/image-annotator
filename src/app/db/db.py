from sqlalchemy import String, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import config

engine = create_engine(config.db_url)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Base(DeclarativeBase):
    pass