import pytest
import time
import threading
import tkinter as tk
from client_logic import connect_to_server, send_message, receive_message

@pytest.fixture
def start_app():
    app = tk.Tk()
    app.after_cancel(app._after)  # Stop the app's main loop
    t = threading.Thread(target=app.mainloop)  # Create a thread for the app
    t.daemon = True
    t.start()
    time.sleep(1)
    yield
    app.quit()

def test_client_connection(start_app):
    host = 'localhost'
    port = 6667
    client_socket = connect_to_server(host, port)
    assert client_socket is not None
    time.sleep(1)  # Wait for the connection

def test_send_receive_message(start_app):
    message = "Test message"
    message_entry = tk.Entry()
    message_entry.delete(0, 'end')  # Clear the message entry
    message_entry.insert(0, message)  # Set the test message
    time.sleep(1)  # Wait for the UI to update
    assert send_message(None, message) is None  # Simulate sending the message
    received_message = receive_message(None)  # Simulate receiving a message
    assert received_message == message  # Check if the received message matches

def test_update_running_time(start_app):
    time.sleep(5)  # Wait for the running time to update
    text = messages.get('1.0', 'end-1c')  # Retrieve the content of the Text widget
    assert "Server runtime:" in text  # Check if the server runtime is displayed
    assert "Client runtime:" in text  # Check if the client runtime is displayed
