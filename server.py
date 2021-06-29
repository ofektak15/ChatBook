import json
import select
import socket

from logout_request import LogoutRequest
from login_request import LoginRequest
from register_request import RegisterRequest
from send_message_request import SendMessageRequest
from get_chats_request import GetChatsRequest
from get_chat_messages_request import GetChatMessagesRequest
from get_username_request import GetUsernameRequest

PORT = 8093
HOST = '127.0.0.1'

MESSAGES = {
                'GetChatMessagesRequest': GetChatMessagesRequest,
                'GetChatsRequest': GetChatsRequest,
                'LogoutRequest': LogoutRequest,
                'SendMessageRequest': SendMessageRequest, 'LoginRequest': LoginRequest,
                'RegisterRequest': RegisterRequest,
                'GetUsernameRequest': GetUsernameRequest
                }

def main():
    server_socket = socket.socket()
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(50)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    client_sockets = []
    authenticated_sockets = {}  # socket: username

    while True:
        all_sockets = [server_socket] + client_sockets
        read_list, write_list, error_list = select.select(all_sockets, client_sockets, [])

        messages = []
        for sock in read_list:
            if sock == server_socket:
                (client_socket, address) = server_socket.accept()
                print("Accepted new socket from: ", address)
                client_sockets.append(client_socket)
                continue

            try:
                data = sock.recv(1024).decode()
                if data == '':
                    data = None
            except Exception as e:
                data = None

            if data is None:
                print('Client closed: ', sock)
                if sock in authenticated_sockets:
                    username = authenticated_sockets[sock]
                    logout_request = LogoutRequest()
                    logout_request.sender_socket = sock
                    logout_request.username = username
                    logout_request.handle(authenticated_sockets)
                    authenticated_sockets.pop(sock)
                client_sockets.remove(sock)
                sock.close()

                continue

            print('***')
            print(data)
            print('***')

            received_json = json.loads(data)
            command_id = received_json['command_id']
            cls_message = MESSAGES.get(command_id, None)
            if cls_message is None:
                print('Unexpected command_id: ', command_id)
                continue

            message = cls_message()
            message.unpack(data)
            message.sender_socket = sock
            messages.append(message)

        for message in messages:
            message.handle(authenticated_sockets)


if __name__ == '__main__':
    main()
