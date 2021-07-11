from src.requests.message import Message
import json


class GetChatMessagesRequest(Message):
    def __init__(self):
        """
        Constructor
        """
        super().__init__()
        self.command_id = 'GetChatMessagesRequest'
        self.chat_name = None

    def pack(self):
        """
        The function doesn't get parameters.
        :return: The function returns a json with all the fields in the class GetChatMessagesRequest.
        """
        obj = {'command_id': self.command_id, 'chat_name': self.chat_name}
        return json.dumps(obj)

    def unpack(self, data):
        """
        The function takes all the arguments from the json (data) and puts them in the members of this class.
        :param data: a json file.
        :return: The function doesn't return a value.
        """
        obj = json.loads(data)
        self.command_id = obj['command_id']
        self.chat_name = obj['chat_name']

    def handle(self, authenticated_sockets):
        """
        The function handles the request
        :param authenticated_sockets: A dictionary of all the users the logged in once.
        key: socket, value: username
        :return: The function handles getting messages from a specific chat.
        """

        str_db = open('db.json', 'r').read()
        json_db = json.loads(str_db)

        # if the sender is not authenticated - return FAIL
        if self.sender_socket not in authenticated_sockets.keys():
            self.sender_socket.send(b'FAIL')
            return

        username = authenticated_sockets[self.sender_socket]

        # If the name of the chat doesn't exist in the DB - return FAIL
        if self.chat_name not in json_db['chats']:
            self.sender_socket.send(b'FAIL')
            return

        # If the username is not one of the participants in the chat - return FAIL
        if username not in json_db['chats'][self.chat_name]['chat_participants']:
            self.sender_socket.send(b'FAIL')
            return

        list_messages = json_db['chats'][self.chat_name]['chat_messages']  # list of messages
        dict_messages = {'username': username, 'list_messages': list_messages}  # dictionary of the messages
        bytes_dict_messages = json.dumps(dict_messages).encode()
        self.sender_socket.send(bytes_dict_messages)  # sending a dictionary of messages
