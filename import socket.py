import socket
import threading


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 6667))
server_socket.listen(5)
print("Server is listening on port 6667")


clients = []


def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message)
            except:
                client.close()
                clients.remove(client)


def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                print(f"{client_socket.getpeername()}: {message}")
                broadcast(message, client_socket)
            else:
                clients.remove(client_socket)
                client_socket.close()
        except:
            continue


while True:
    client, addr = server_socket.accept()
    clients.append(client)
    print(f"Connected to {addr}")
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()
