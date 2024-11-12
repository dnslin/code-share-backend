from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from app.database import Base

class Snippet(Base):
    __tablename__ = "snippets"

    id = Column(Integer, primary_key=True, index=True)
    sequence = Column(String(100), unique=True, index=True)
    title = Column(String(200), nullable=True)
    code = Column(Text)
    language = Column(String(50))
    description = Column(Text, nullable=True)
    share_link = Column(String(100), unique=True, nullable=True)
    access_code = Column(String(100), nullable=True)
    expire_at = Column(DateTime, nullable=True)
    shared_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)