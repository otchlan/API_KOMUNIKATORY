import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import imaplib
import email
from mail_api import (
    connect_to_server,
    get_all_emails,
    get_email_content,
    extract_email_details,
    extract_email_body
)

# Mock email data for testing purposes
MOCK_EMAIL = b"Your mock email data here in bytes format"

# Mock email message for testing purposes
class MockEmailMessage:
    def __init__(self):
        self._payload = MOCK_EMAIL
        self._headers = {
            'subject': 'Test Subject',
            'from': 'test@example.com',
            'to': 'recipient@example.com'
        }

    def __getitem__(self, key):
        return self._headers.get(key)

    def is_multipart(self):
        return False

    def get_payload(self, decode=False):
        return self._payload

# Mock IMAP connection for testing purposes
class MockIMAPConnection:
    def login(self, email, password):
        pass

    def select(self, mailbox):
        pass

    def search(self, charset, search_criterion):
        return (None, [b'1'])

    def fetch(self, num, data_format):
        return (None, [(None, MOCK_EMAIL)])

    def logout(self):
        pass

def test_connect_to_server(monkeypatch):
    def mockreturn(host, port):
        return MockIMAPConnection()

    monkeypatch.setattr(imaplib, "IMAP4_SSL", mockreturn)

    result = connect_to_server("test@example.com", "password")
    assert isinstance(result, MockIMAPConnection)

def test_get_all_emails():
    mail = MockIMAPConnection()
    result = get_all_emails(mail)
    assert result == [b'1']

def test_get_email_content():
    mail = MockIMAPConnection()
    result = get_email_content(mail, b'1')
    assert isinstance(result, email.message.Message)

def test_extract_email_details():
    email_message = MockEmailMessage()
    subject, sender, recipients = extract_email_details(email_message)
    assert subject == "Test Subject"
    assert sender == "test@example.com"
    assert recipients == "recipient@example.com"

def test_extract_email_body():
    email_message = MockEmailMessage()
    result = extract_email_body(email_message)
    assert result == MOCK_EMAIL.decode()

# Add more tests as needed
