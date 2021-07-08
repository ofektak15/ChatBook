from src.requests.create_group_chat import CreateGroupChat
from src.requests.create_private_chat import CreatePrivateChat
from src.requests.get_chat_messages_request import GetChatMessagesRequest
from src.requests.get_chats_request import GetChatsRequest
from src.requests.get_username_request import GetUsernameRequest
from src.requests.login_request import LoginRequest
from src.requests.logout_request import LogoutRequest
from src.requests.register_request import RegisterRequest
from src.requests.send_message_request import SendMessageRequest


class Consts(object):
    MESSAGES = {
        'GetChatMessagesRequest': GetChatMessagesRequest,
        'GetChatsRequest': GetChatsRequest,
        'LogoutRequest': LogoutRequest,
        'SendMessageRequest': SendMessageRequest,
        'LoginRequest': LoginRequest,
        'RegisterRequest': RegisterRequest,
        'GetUsernameRequest': GetUsernameRequest,
        'CreatePrivateChat': CreatePrivateChat,
        'CreateGroupChat': CreateGroupChat
    }

    PORT = 8082
    HOST = '127.0.0.1'
