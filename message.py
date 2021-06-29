from login_request import LoginRequest
from register_request import RegisterRequest
from send_message_request import SendMessageRequest
from get_chats_request import GetChatsRequest
from get_chat_messages_request import GetChatMessagesRequest
from get_username_request import GetUsernameRequest
from logout_request import LogoutRequest


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


MESSAGES = {
                'GetChatMessagesRequest': GetChatMessagesRequest,
                'GetChatsRequest': GetChatsRequest,
                'LogoutRequest': LogoutRequest,
                'SendMessageRequest': SendMessageRequest, 'LoginRequest': LoginRequest,
                'RegisterRequest': RegisterRequest,
                'GetUsernameRequest': GetUsernameRequest
                }




















