from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from .base import Base
import datetime

class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    source = Column(Enum('email', 'whatsapp', name='source_type'), nullable=False)
    subject = Column(String)
    sender = Column(String, nullable=False)
    recipients = Column(String)
    content = Column(Text)
    footer = Column(Text)
    original_content = Column(Text)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    attachments_path = Column(String)

    attachments = relationship("Attachment", back_populates="message")
