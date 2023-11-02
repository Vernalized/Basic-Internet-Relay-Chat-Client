import tkinter as tk
from tkinter import Scrollbar, Text
import socket
import threading
from datetime import datetime
import pytz
import requests

# Store the start time of the server and client.
server_start_time = datetime.now()
client_start_time = datetime.now()

# Create the main application window.
app = tk.Tk()
app.title("Basic Chat Relay Client")

# Create the debug frame for debug console.
debug_frame = tk.Frame(app)
debug_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)  # Right align and expand.

# Create the Text widget for displaying debug messages.
debug_messages = Text(debug_frame, wrap=tk.WORD, state=tk.DISABLED)
debug_messages.pack(fill=tk.BOTH, expand=True)
debug_scrollbar = Scrollbar(debug_frame, command=debug_messages.yview)  # Create a vertical scrollbar.
debug_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # Attach the scrollbar

# Configure the Text widget to use the scrollbar.
debug_messages.config(yscrollcommand=debug_scrollbar.set)

# Create the message frame for the message thread.
message_frame = tk.Frame(app)
message_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # Left align and expand.

# Create a Text widget for displaying messages.
messages = Text(message_frame, wrap=tk.WORD, state=tk.DISABLED)
messages.pack(fill=tk.BOTH, expand=True)
message_scrollbar = Scrollbar(message_frame, command=messages.yview)  # Create a vertical scrollbar.
message_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # Attach the scrollbar.

# Configure the Text widget to use the scrollbar.
messages.config(yscrollcommand=message_scrollbar.set)

# Function to update the debug console on a basis.
def update_debug_console(message, text_widget):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_message = f"[{timestamp}] {message}"
    text_widget.config(state=tk.NORMAL)
    text_widget.insert(tk.END, formatted_message + '\n')
    text_widget.config(state=tk.DISABLED)

# Function to display a welcome message with the user's information.
def welcome_message():
    local_tz = pytz.timezone(pytz.country_timezones('US')[0])
    local_time = datetime.now(local_tz).strftime("%Y-%m-%d %H:%M:%S")
    ip_info = requests.get("https://ipinfo.io").json()
    welcome_msg = f"Hello World! ^_^\n" # ← Welcome Message
    welcome_msg += f"IP: {ip_info['ip']}\n" # ← Your IP
    welcome_msg += f"Country: {ip_info['country']}\n" # ← Your Country
    welcome_msg += f"State/Province: {ip_info['region']}\n" # ← Your State and/or Province
    welcome_msg += f"Timezone: {local_tz}\n" # ← Your Timezone
     
    messages.insert(tk.END, welcome_msg + '\n')
    messages.config(state=tk.DISABLED)

    # Update the debug console.
    update_debug_console("Client started", debug_messages)
    update_debug_console("Welcome message displayed", debug_messages)

# Run the welcome_message function to display the welcome message.
welcome_message()

# Connect to the server.
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect(('localhost', 6667)) # Attempts to establish a connection to a server running on the localhost.
    update_debug_console("Connected to the server!", debug_messages)
except ConnectionRefusedError:
    update_debug_console("Failed to connect to the server. *Womp Womp*", debug_messages)

# Create a message entry frame.
message_entry_frame = tk.Frame(message_frame) # Creates a new frame widget named 'message_entry_frame' and positions it within the 'message_frame' container. 
message_entry_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, anchor="s")  # Anchor "s", aligns it to the bottom.

# Create an Entry widget for typing messages.
message_entry = tk.Entry(message_entry_frame) # Creates an Entry widget
message_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True) # Positions the widget inside the 'message_entry_frame' container.

# Create a button for sending messages.
def send_message(event=None): # Defines the send_message function, takes an optional event parameter (typically an event object) as its argument.
    message = message_entry.get() # Retrieves the message you've typed.
    if message: # Checks if you actually typed something (if the message is not empty).
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Stamps the current time & date to your message.
        formatted_message = f"<You> [{timestamp}]: {message}"  # Combimes your username, message, and timestamp yadayada
        messages.config(state=tk.NORMAL) # Updates the Message Thread.
        messages.insert(tk.END, formatted_message + '\n') # Adds your message to the message thread so you can see it.
        messages.config(state=tk.DISABLED) # Locks the Message Thread window from messing it up, prettyyy much self explanatory.
        client_socket.send(formatted_message.encode()) # Sends your message to to the server for everyone to see, God knows what you just sent.
        message_entry.delete(0, tk.END) # Clears your text box.

        # Update the debug console pt 2 electric boogaloo
        debug_message = f"Sent: {formatted_message}" # Alerts the debug console that a message has been sent.
        update_debug_console(debug_message, debug_messages) # Actually updates the debug console.

send_button = tk.Button(message_entry_frame, text="Send", command=send_message) # Creates the Send button, functions it to update the message display thread in the GUI.
send_button.pack(side=tk.RIGHT, fill=tk.BOTH)

# Binds the ENTER key to the send_message function. Basically letting you use ENTER to send a message like any other.
message_entry.bind("<Return>", send_message) # fully implements the bind function.

# Function to update the connection status in the debug console.
def update_connection_status(connected): # Updates the status of the connection. 
    if connected:
        update_debug_console("Connected to the server!", debug_messages) # Debug console updates that the Server is connected.
    else:
        update_debug_console("Connection lost! *Womp Womp*", debug_messages) # Debug console updates that the Server is not connected.

# Function to receive messages.
def receive_messages():# Function to receive a message.
    while True:
        try:
            message = client_socket.recv(1024).decode() # Receives a message from the 'client_socket' (the socket used to communicate with the server). It reads up to 1024 bytes of data and decodes it, assuming it's in a text format.
            messages.config(state=tk.NORMAL) # Sets the state of the 'messages', Text widget to NORMAL, allowing it to be edited.
            messages.insert(tk.END, message + '\n') # Inserts the received 'message' at the end of the 'messages' Text widget, displaying the message in the chat interface. '\n' is added to ensure that each message is on a new line.
            messages.config(state=tk.DISABLED) # It sets the state of the 'messages' Text widget back to DISABLED, preventing further editing.

            # Update the debug console pt 3
            debug_message = f"Received: {message}" # Alerts the debug console to send a debug console update message.
            update_debug_console(debug_message, debug_messages) # Updates the debug console.

        except:
            update_connection_status(connected=False) # Updates connect status, alerts that the connection has been lost/severed.
            print("Connection lost. *Womp Womp*")
            client_socket.close()
            break

# Create a thread for receiving messages.
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Function to update the running time.
def update_running_time():
    current_time = datetime.now() # Calculates the datetime for each update tick, both Client and Server runtimes.
    server_running_time = current_time - server_start_time # Starting the Server runtime update.
    client_running_time = current_time - client_start_time # Starting the Client runtime update.
    server_running_time_str = str(server_running_time).split('.')[0] # Server runtime string count.
    client_running_time_str = str(client_running_time).split('.')[0] # Client runtime string count.
    update_debug_console(f"Server runtime: {server_running_time_str}", debug_messages) # Server runtime debug console update.
    update_debug_console(f"Client runtime: {client_running_time_str}", debug_messages) # Client runtime debug console update.
    app.after(1000, update_running_time)  # Schedule the next update.

# Start the running time updater.
app.after(1000, update_running_time)

# Start the GUI application.
app.mainloop()
