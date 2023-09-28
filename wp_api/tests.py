import pytest
from unittest.mock import patch, Mock
from wp_api import app, send_and_monitor_whatsapp_message, save_to_txt_file, received_messages

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Received Messages" in response.data


@patch('wp_api.initialize_webdriver')
@patch('wp_api.open_whatsapp_and_scan_qr')
@patch('wp_api.select_chat')
@patch('wp_api.send_message')
@patch('wp_api.monitor_incoming_messages')
def test_send_and_monitor_whatsapp_message(mock_monitor, mock_send, mock_select, mock_scan, mock_init, client):
    mock_driver = Mock()
    mock_init.return_value = mock_driver

    send_and_monitor_whatsapp_message("Test", "Hello from Flask!")
    
    mock_init.assert_called_once()
    mock_scan.assert_called_once_with(mock_driver)
    mock_select.assert_called_once_with(mock_driver, "Test")
    mock_send.assert_called_once_with(mock_driver, "Hello from Flask!")
    mock_monitor.assert_called_once_with(mock_driver)

def test_save_to_txt_file(tmp_path):
    d = tmp_path / "subdir"
    d.mkdir()
    test_file = d / "received_messages.txt"

    with patch('wp_api.open', return_value=test_file.open('w')):
        save_to_txt_file("Test Message")
    
    assert test_file.read_text() == "Test Message\n"

def test_received_messages():
    received_messages.append("Test Message")
    assert "Test Message" in received_messages
