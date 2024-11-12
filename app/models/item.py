from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True)
    description = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)