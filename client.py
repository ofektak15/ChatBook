import json

from message import LoginRequest, RegisterRequest, SendMessageRequest, GetChatsRequest
import socket

from server import PORT, HOST


class Client(object):
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOST, PORT))

    def register(self, username, password):
        request = RegisterRequest()
        request.username = username
        request.password = password

        print('register')
        print(request.username)
        print(request.password)

        self.sock.send(request.pack().encode())
        status = self.sock.recv(1024).decode()
        if status == 'SUCCESS':
            return True
        return False

    def login(self, username, password):
        request = LoginRequest()

        request.username = username
        request.password = password

        print('login')
        print(request.username)
        print(request.password)

        self.sock.send(request.pack().encode())
        status = self.sock.recv(1024).decode()
        print(status)
        if status == 'SUCCESS':
            return True
        return False

    def send_message(self, username, content, recipient):
        request = SendMessageRequest()

        request.sender_username = username
        request.recipient = recipient
        request.message_content = content

        self.sock.send(request.pack().encode())
        status = self.sock.recv(1024).decode()
        if status == 'SUCCESS':
            return True
        return False

    def handle_recv(self):
        data = self.sock.recv(1024).decode()

        # TODO: Handle server closed
        if data:  # if len(data) != 0
            message = SendMessageRequest()
            message.unpack(data)
            msg = 'Got message "' + message.message_content + '" From "' + message.sender_username + '"'
            print(msg)
            return msg

    def get_chats(self):
        request = GetChatsRequest()

        self.sock.send(request.pack().encode())
        bytes_list_chat_names = self.sock.recv(1024).decode()
        list_chat_names = json.loads(bytes_list_chat_names)
        return json.dumps(list_chat_names)
