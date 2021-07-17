from src.requests.create_group_chat import CreateGroupChat
from src.requests.create_private_chat import CreatePrivateChat
from src.requests.get_chat_messages_request import GetChatMessagesRequest
from src.requests.get_chats_request import GetChatsRequest
from src.requests.get_is_connected import GetIsConnected
from src.requests.get_number_of_new_messages_request import GetNumberOfNewMessages
from src.requests.get_username_request import GetUsernameRequest
from src.requests.get_is_update import GetIsUpdate
from src.requests.login_request import LoginRequest
from src.requests.logout_request import LogoutRequest
from src.requests.register_request import RegisterRequest
from src.requests.send_message_request import SendMessageRequest


class Consts(object):
    # A dictionary that contains all the types of the requests
    MESSAGES = {
        'GetChatMessagesRequest': GetChatMessagesRequest,
        'GetChatsRequest': GetChatsRequest,
        'LogoutRequest': LogoutRequest,
        'SendMessageRequest': SendMessageRequest,
        'LoginRequest': LoginRequest,
        'RegisterRequest': RegisterRequest,
        'GetUsernameRequest': GetUsernameRequest,
        'CreatePrivateChat': CreatePrivateChat,
        'CreateGroupChat': CreateGroupChat,
        'GetIsConnected': GetIsConnected,
        'GetIsUpdate': GetIsUpdate,
        'GetNumberOfNewMessages': GetNumberOfNewMessages,
    }

    PORT = 8082
    HOST = '127.0.0.1'


