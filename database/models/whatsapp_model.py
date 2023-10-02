from sqlalchemy import Column, Integer, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class WhatsAppMessage(Base):
    __tablename__ = 'whatsapp_messages'

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    message_id = Column(Integer, ForeignKey('messages.id'))
    message = relationship("Message", backref="whatsapp_message")
