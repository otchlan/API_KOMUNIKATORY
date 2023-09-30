from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class WhatsAppMessage(Base):
    __tablename__ = 'whatsapp_messages'

    id = Column(Integer, primary_key=True, index=True)
    sender = Column(String, index=True)
    message_content = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    attachments_path = Column(String)

    message_id = Column(Integer, ForeignKey('messages.id'))
    message = relationship("Message", backref="whatsapp_message")
