import json
import socket
from src.consts import Consts
from src.requests.get_chat_messages_request import GetChatMessagesRequest
from src.requests.get_chats_request import GetChatsRequest
from src.requests.get_username_request import GetUsernameRequest
from src.requests.login_request import LoginRequest
from src.requests.register_request import RegisterRequest
from src.requests.send_message_request import SendMessageRequest


class Client(object):
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((Consts.HOST, Consts.PORT))

    def register(self, username, password):
        request = RegisterRequest()
        request.username = username
        request.password = password

        print('register')
        print(request.username)
        print(request.password)

        self.sock.send(request.pack().encode())
        status = self.sock.recv(1024 * 1024).decode()
        if status == 'SUCCESS':
            return True
        return False

    def login(self, username, password):
        request = LoginRequest()

        request.username = username
        request.password = password

        print('login - client')
        print(request.username)
        print(request.password)

        print("request sent to server: " + request.pack())
        self.sock.send(request.pack().encode())
        status = self.sock.recv(1024 * 1024).decode()
        print(status)
        if status == 'SUCCESS':
            return True
        return False

    def send_message(self, username, recipient, content, chat_type):
        request = SendMessageRequest()

        request.sender_username = username
        request.recipients = recipient
        request.group_name = recipient
        request.type_of_message = chat_type
        request.message_content = content

        self.sock.send(request.pack().encode())
        status = self.sock.recv(1024 * 1024).decode()
        if status == 'SUCCESS':
            return True
        return False

    def handle_recv(self):
        data = self.sock.recv(1024 * 1024).decode()

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
        bytes_dict_chats = self.sock.recv(1024 * 1024).decode()
        print('get_chats: ' + bytes_dict_chats)
        dict_chats = json.loads(bytes_dict_chats)
        return dict_chats

    def get_chat_messages(self, chat_name):
        request = GetChatMessagesRequest()
        request.chat_name = chat_name
        self.sock.send(request.pack().encode())
        bytes_list_messages = self.sock.recv(1024 * 1024).decode()
        print('get_chat_messages: ' + bytes_list_messages)
        dict_messages = json.loads(bytes_list_messages)
        return dict_messages

    def get_username(self):
        request = GetUsernameRequest()
        self.sock.send(request.pack().encode())
        username = self.sock.recv(1024 * 1024).decode()
        return username
