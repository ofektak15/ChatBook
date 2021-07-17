from src.consts import Consts
import json
import select
import socket
from src.requests.logout_request import LogoutRequest


def main():
    server_socket = socket.socket()
    server_socket.bind(("0.0.0.0", Consts.PORT))
    server_socket.listen(50)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    client_sockets = []  # a list of all the sockets of the clients
    authenticated_sockets = {}  # key: socket, value: username

    while True:
        all_sockets = [server_socket] + client_sockets
        read_list, write_list, error_list = select.select(all_sockets, client_sockets, [])

        messages = []  # a list that contains all the messages the server needs to handle
        for sock in read_list:
            if sock == server_socket:
                (client_socket, address) = server_socket.accept()  # accepting the client
                print("Accepted new socket from: ", address)
                client_sockets.append(
                    client_socket)  # adding the socket of the client to the list of all client sockets
                continue

            data = sock.recv(1024).decode()  # receiving the data
            if data == '':
                data = None

            if data is None:  # client closed
                print('Client closed: ', sock)
                if sock in authenticated_sockets:  # if he is authenticated
                    username = authenticated_sockets[sock]  # username
                    logout_request = LogoutRequest()  # creating a logout request
                    logout_request.sender_socket = sock
                    logout_request.username = username
                    logout_request.handle(authenticated_sockets)  # handling logout request
                    authenticated_sockets.pop(sock)  # removing the client from the authenticated_sockets dictionary
                client_sockets.remove(sock)  # removing the client from the client_sockets list
                sock.close()  # closing the connection with the socket
                continue

            print('***')
            print(data)
            print('***')

            received_json = json.loads(data)
            command_id = received_json['command_id']  # command id
            cls_message = Consts.MESSAGES.get(command_id)  # getting the class of the request

            message = cls_message()
            message.unpack(data)
            message.sender_socket = sock
            messages.append(message)  # adding the request (message) to the messages list

        # handling all the messages list
        for message in messages:
            message.handle(authenticated_sockets)


if __name__ == '__main__':
    main()
