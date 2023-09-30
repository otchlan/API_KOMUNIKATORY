from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database.models.base import Base

class Email(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, index=True)
    sender = Column(String, index=True)
    recipients = Column(String)
    content = Column(Text)
    footer = Column(Text)
    original_content = Column(Text)
    timestamp = Column(DateTime)
    attachments_path = Column(String)

    message_id = Column(Integer, ForeignKey('messages.id'))
    message = relationship("Message", backref="email")
