import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))  

import pytest
from database.db_session import init_db, db
from database.models.message_model import Message
from database.operations.queries import get_all_messages
from sqlalchemy import create_engine


DATABASE_URL = "sqlite:///./test_temp.db"

# ---------------- Setup and Teardown ----------------

@pytest.fixture(scope="module")
def test_db():
    # Override your DATABASE_URL
    db.engine = create_engine(DATABASE_URL)
    init_db()

    yield db

    os.remove("./test_temp.db")


# ---------------- Tests for db_session.py ----------------

def test_init_db(test_db):
    """Test if the database has been initialized correctly."""
    assert os.path.exists("./test_temp.db")


# ---------------- Tests for operations/queries.py ----------------

def test_get_all_messages_empty_db(test_db):
    """Test if the function returns None when there are no messages."""
    messages, columns = get_all_messages()
    assert messages == []
    assert columns == [column.name for column in Message.__table__.columns]


def test_add_and_get_message(test_db):
    """Test adding a message and retrieving it."""
    # Assuming your Message model has a 'text' attribute, adjust accordingly
    test_message = Message(text="Test message.")
    test_db.add(test_message)
    test_db.commit()

    messages, columns = get_all_messages()
    assert len(messages) == 1
    assert messages[0].text == "Test message."
