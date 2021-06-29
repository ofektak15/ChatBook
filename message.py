import json
import time
import hashlib


class Message(object):
    def __init__(self):
        self.command_id = None
        self.sender_username = None
        self.sender_socket = None

    def pack(self):
        raise NotImplementedError

    def unpack(self, data):
        raise NotImplementedError

    def handle(self, authenticated_sockets):
        raise NotImplementedError






















MESSAGES = {'GetChatMessagesRequest': GetChatMessagesRequest, 'GetChatsRequest': GetChatsRequest,
            'LogoutRequest': LogoutRequest,
            'SendMessageRequest': SendMessageRequest, 'LoginRequest': LoginRequest,
            'RegisterRequest': RegisterRequest,
            'GetUsernameRequest': GetUsernameRequest}
