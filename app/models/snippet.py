from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
import uuid

from app.database import Base

class Snippet(Base):
    __tablename__ = "snippets"

    id = Column(Integer, primary_key=True, index=True)
    sequence = Column(String(36), unique=True, nullable=False)
    code = Column(Text, nullable=False)
    language = Column(String(50), nullable=False)
    title = Column(String(200))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())