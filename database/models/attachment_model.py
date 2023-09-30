from sqlalchemy import Column, Integer, String, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship
from .base import Base

class Attachment(Base):
    __tablename__ = 'attachments'

    id = Column(Integer, primary_key=True)
    message_id = Column(Integer, ForeignKey('messages.id'))
    file_path = Column(String)
    file_data = Column(LargeBinary)
    file_name = Column(String)
    file_type = Column(String)

    message = relationship("Message", back_populates="attachments")
