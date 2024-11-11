from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from app.database import Base

class Language(Base):
    __tablename__ = "languages"

    id = Column(String(50), primary_key=True)
    name = Column(String(100))
    category = Column(String(50))
    extensions = Column(String(200))
    mime_type = Column(String(100))
    aliases = Column(String(200))

class Snippet(Base):
    __tablename__ = "snippets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    code = Column(Text)
    language = Column(String(50))
    description = Column(Text, nullable=True)
    access_code = Column(String(100), unique=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    expire_at = Column(DateTime, nullable=True)