import json
import socket
from src.consts import Consts
from src.requests.create_group_chat import CreateGroupChat
from src.requests.get_chat_messages_request import GetChatMessagesRequest
from src.requests.get_chats_request import GetChatsRequest
from src.requests.get_is_connected import GetIsConnected
from src.requests.get_is_update import GetIsUpdate
from src.requests.get_number_of_new_messages_request import GetNumberOfNewMessages
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
        """
        :param username: the username of the client
        :param password: the password of the client
        :return: the function returns true if the inputs are valid. Else - returns false.
        """
        request = RegisterRequest()

        request.username = username
        request.password = password

        print('register')
        print(request.username)
        print(request.password)

        self.sock.send(request.pack().encode())
        status = self.sock.recv(1024 * 1024).decode()  # receiving the status

        if status == 'SUCCESS':
            return True
        return False

    def login(self, username, password):
        """
        :param username: the username of the client
        :param password: the password of the client
        :return: the function returns true if the user exists in the DB and the inputs are valid. Else - returns false.
        """
        request = LoginRequest()

        request.username = username
        request.password = password

        print("request sent to server: " + request.pack())
        self.sock.send(request.pack().encode())

        status = self.sock.recv(1024 * 1024).decode()  # receiving the status
        print(status)

        if status == 'SUCCESS':
            return True
        return False

    def send_message(self, username, recipient, content, chat_type):
        """
        :param username: the username of the client
        :param recipient: the username/s of the recipient/s
        :param content: the content of the message
        :param chat_type: the type of the chat (private/group)
        :return: the function returns true if the message has been sent successfully. Else - returns false.
        """
        request = SendMessageRequest()

        request.sender_username = username
        request.recipients = recipient
        request.group_name = recipient
        request.type_of_message = chat_type
        request.message_content = content

        print("send message request: " + request.pack())

        self.sock.send(request.pack().encode())
        status = self.sock.recv(1024 * 1024).decode()  # receiving the status

        if status == 'SUCCESS':
            return True
        return False

    def get_chats(self):
        """
        The function dorsn't get parameters
        :return: the function returns a dictionary that contains all the chats that the client has.
        """
        request = GetChatsRequest()

        print(request.pack())

        self.sock.send(request.pack().encode())
        bytes_dict_chats = self.sock.recv(1024 * 1024).decode()

        print('get_chats: ' + bytes_dict_chats)

        dict_chats = json.loads(bytes_dict_chats)
        return dict_chats

    def get_chat_messages(self, chat_name):
        """
        :param chat_name: the name of the chat
        :return: the function returns a dictionary that contains all the messages that are in the group/private chat.
        """
        request = GetChatMessagesRequest()
        request.chat_name = chat_name

        print("get_chat_messages request: " + request.pack())

        self.sock.send(request.pack().encode())

        bytes_list_messages = self.sock.recv(1024 * 1024).decode()
        dict_messages = json.loads(bytes_list_messages)
        return dict_messages

    def get_username(self):
        """
        The function doesn't get parameters
        :return: the function returns the username of the client.
        """
        request = GetUsernameRequest()
        self.sock.send(request.pack().encode())

        username = self.sock.recv(1024 * 1024).decode()  # the received username
        request.username = username

        return username

    def log_out(self, username):
        """
        :param username: the username of the client
        :return: the function handling a logout request.
        """
        request = LogoutRequest()
        request.username = username

        print("request:" + request.pack())
        self.sock.send(request.pack().encode())

    def create_private_chat(self, recipient):
        """
        :param recipient: the username of the recipient
        :return: the function returns true if the private chat was created successfully. Else - returns false.
        """
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

    def create_group_chat(self, recipients, group_name):
        """
        :param recipients: the usernames of the recipients
        :param group_name: the name of the group
        :return: the function returns true if thr group chat was created successfully. Else - returns false.
        """
        request = CreateGroupChat()
        request.recipient = recipients
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
        """
        :param username: the username of the client
        :return: the function returns true if the user is connected, else - returns false.
        """
        request = GetIsConnected()
        request.username = username
        print("request: " + request.pack())

        self.sock.send(request.pack().encode())
        str_dict_is_connected = self.sock.recv(1024).decode()
        dict_is_connected = json.loads(str_dict_is_connected)

        status = dict_is_connected['is_connected']
        print(status)
        return status

    def get_is_update(self):
        """
        The function doesn't get parameters.
        :return: the function returns true if the user needs an update, else - returns false.
        """
        request = GetIsUpdate()
        print("request: " + request.pack())
        self.sock.send(request.pack().encode())

        str_dict_is_update = self.sock.recv(1024).decode()
        dict_is_update = json.loads(str_dict_is_update)
        status = dict_is_update['is_update']
        print(status)
        return status

    def get_number_of_new_messages(self, username, chat_name):
        """
        :param username: the username of the client
        :param chat_name: the name of the chat
        :return: the function returns the number of the unread messages in a specific chat.
        """
        request = GetNumberOfNewMessages()
        request.username = username
        request.chat_name = chat_name

        self.sock.send(request.pack().encode())
        number_of_new_messages = self.sock.recv(1024).decode()
        return number_of_new_messages
