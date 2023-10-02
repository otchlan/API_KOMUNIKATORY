from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database.models.base import Base

class Email(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)

    message_id = Column(Integer, ForeignKey('messages.id'))
    message = relationship("Message", backref="email_instance")
