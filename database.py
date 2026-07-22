import os
import uuid
from datetime import datetime

from sqlalchemy import create_engine, Column, String, DateTime, JSON
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class Document(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    filename = Column(String, nullable=False)
    status = Column(String, nullable=False, default="pending")  # pending / done / failed
    result = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


# call this once to create the table if it doesn't exist yet
def init_db():
    Base.metadata.create_all(bind=engine)