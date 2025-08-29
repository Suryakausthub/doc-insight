import uuid, datetime as dt
from sqlalchemy import Column, String, DateTime, Text
from db import Base   # ✅ no leading dot

class Upload(Base):
    __tablename__ = "uploads"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    filename = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=dt.datetime.utcnow)
    text_chars = Column(String)
    summary_type = Column(String)          # "ai" or "fallback"
    summary = Column(Text, nullable=True)
    top_words_json = Column(Text, nullable=True)
