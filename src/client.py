import json
import socket
from src.consts import Consts
from src.requests.create_group_chat import CreateGroupChat
from src.requests.get_chat_messages_request import GetChatMessagesRequest
from src.requests.get_chats_request import GetChatsRequest
from src.requests.get_is_connected import GetIsConnected
from src.requests.get_username_request import GetUsernameRequest
from src.requests.login_request import LoginRequest
from src.requests.register_request import RegisterRequest
from src.requests.send_message_request import SendMessageRequest
from src.requests.create_private_chat import CreatePrivateChat
from src.requests.logout_request import LogoutRequest


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

        print("request sent to server: " + request.pack())
        self.sock.send(request.pack().encode())
        status = self.sock.recv(1024 * 1024).decode()
        print(status)
        if status == 'SUCCESS':
            return True
        return False

    def send_message(self, username, recipient, content, chat_type):
        request = SendMessageRequest()
        print("send message request: " + request.pack())
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
        print(request.pack())
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

    def log_out(self, username):
        request = LogoutRequest()
        request.username = username
        print("request:" + request.pack())
        self.sock.send(request.pack().encode())

    def create_private_chat(self, recipient):
        request = CreatePrivateChat()
        request.recipient = recipient
        print("request: " + request.pack())
        self.sock.send(request.pack().encode())
        status = self.sock.recv(1024).decode()
        print(status)
        if status == "SUCCESS":
            return True
        elif status == "FAIL":
            return False

    def create_group_chat(self, recipient, group_name):
        request = CreateGroupChat()
        request.recipient = recipient
        request.group_name = group_name
        print("request: " + request.pack())
        self.sock.send(request.pack().encode())
        status = self.sock.recv(1024).decode()
        print(status)
        if status == "SUCCESS":
            return True
        elif status == "FAIL":
            return False

    def get_is_connected(self, username):
        request = GetIsConnected()
        request.username = username
        print("request: " + request.pack())
        self.sock.send(request.pack().encode())
        status = self.sock.recv(1024).decode()
        print(status)
        return status


