import pytest
from database.db_session import Session
from models.email_model import Message

@pytest.fixture
def session():
    session = Session()
    yield session
    session.close()

def test_add_message(session):
    new_message = Message(
        source="email",
        subject="Test Subject",
        sender="test@example.com",
        recipients="recipient@example.com",
        content="This is a test message.",
        footer="Best regards, Test"
    )
    session.add(new_message)
    session.commit()

    added_message = session.query(Message).filter_by(subject="Test Subject").first()
    assert added_message is not None
