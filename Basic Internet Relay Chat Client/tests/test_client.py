import pytest
import time
import threading
from client import app, client_socket, messages, message_entry

@pytest.fixture
def start_app():
    app.after_cancel(app._after)  # Stop the app's main loop
    t = threading.Thread(target=app.mainloop)  # Create a thread for the app
    t.daemon = True
    t.start()
    time.sleep(1)
    yield
    app.quit()

def test_client_connection(start_app):
    assert client_socket.connect(('localhost', 6667)) is None
    time.sleep(1)  # Wait for the connection

def test_send_receive_message(start_app):
    message = "Test message"
    message_entry.delete(0, 'end')  # Clear the message entry
    message_entry.insert(0, message)  # Set the test message
    time.sleep(1)  # Wait for the UI to update
    message_entry.event_generate('<Return>')  # Simulate pressing the Return key
    time.sleep(1)  # Wait for the message to be sent and received
    text = messages.get('1.0', 'end-1c')  # Retrieve the content of the Text widget
    assert message in text  # Check if the message is received

def test_update_running_time(start_app):
    time.sleep(5)  # Wait for the running time to update
    text = messages.get('1.0', 'end-1c')  # Retrieve the content of the Text widget
    assert "Server runtime:" in text  # Check if the server runtime is displayed
    assert "Client runtime:" in text  # Check if the client runtime is displayed
