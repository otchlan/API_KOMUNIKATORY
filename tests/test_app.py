import pytest
from flask_testing import TestCase
from app import app, get_all_messages
from database.session import SessionLocal, engine
from database.models import Message, Base

class AppTest(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    TESTING = True

    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = self.SQLALCHEMY_DATABASE_URI
        app.config['TESTING'] = self.TESTING
        return app

    def setUp(self):
        # Set up data for the tests
        self.db = SessionLocal()
        Base.metadata.create_all(bind=engine)
        sample_message = Message(content="Hello, Test!")  # Assuming a 'content' field
        self.db.add(sample_message)
        self.db.commit()

    def tearDown(self):
        self.db.close()
        Base.metadata.drop_all(bind=engine)

    def test_index(self):
        response = self.client.get("/")
        self.assert200(response)
        self.assert_template_used('index.html')
        assert b"Hello, Test!" in response.data

    def test_get_all_messages(self):
        messages, columns = get_all_messages()
        assert len(messages) == 1
        assert messages[0].content == "Hello, Test!"
        assert 'content' in columns

