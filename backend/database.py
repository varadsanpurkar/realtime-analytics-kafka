from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = "postgresql://analytics:analytics123@localhost:5432/clickstream_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ClickEvent(Base):
    __tablename__ = "click_events"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    event_type = Column(String, index=True)  # page_view, click, purchase
    page_url = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    session_id = Column(String, index=True)
    country = Column(String)
    device = Column(String)
    revenue = Column(Float, nullable=True)
    
    __table_args__ = (
        Index('idx_timestamp_event', 'timestamp', 'event_type'),
    )

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()