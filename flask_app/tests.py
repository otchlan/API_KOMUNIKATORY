import pytest
from app import app, engine, messages_table

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    # Możesz dodać więcej asercji w zależności od tego, czego oczekujesz od odpowiedzi.
    # Na przykład:
    # assert b"Wiadomości" in response.data

def test_database_connection():
    # Próba połączenia z bazą danych
    with engine.connect() as connection:
        # Wykonanie prostego zapytania, aby sprawdzić, czy połączenie działa poprawnie
        result = connection.execute('SELECT 1').fetchone()
        assert result == (1,)
