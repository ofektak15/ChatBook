import socket
import select

MAX_MSG_LENGTH = 1024
SERVER_PORT = 8888
SERVER_IP = "0.0.0.0"


def print_client_sockets(client_sockets):
    for c in client_sockets:
        print("\t", c.getpeername())


def main():
    print("Setting up server...")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen()
    print("Listening for clients...")
    client_sockets = []
    while True:
        ready_to_read, ready_to_write, in_error = select.select([server_socket] + print_client_sockets, [], [])
        for currnet_socket in ready_to_read:
            if currnet_socket is server_socket:
                (client_socket, client_address) = currnet_socket.accept()
                print("New client joined!", client_address)
                client_sockets.append(client_socket)
                print_client_sockets(client_sockets)
            else:
                print("New data from client")
                data = currnet_socket.recv(MAX_MSG_LENGTH).decode()
                if data == "":
                    print("Connection closed")
                    client_sockets.remove(currnet_socket)
                    currnet_socket.close()
                    print_client_sockets(client_sockets)
                else:
                    print(data)
                    currnet_socket.send(data.encode())

