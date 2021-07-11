from src.requests.message import Message
import json
import datetime


class GetChatsRequest(Message):
    def __init__(self):
        """
        Constructor
        """
        super().__init__()
        self.command_id = 'GetChatsRequest'

    def pack(self):
        """
        The function doesn't get parameters.
        :return: The function returns a json with all the fields in the class GetChatsRequest.
        """
        obj = {'command_id': self.command_id}
        return json.dumps(obj)

    def unpack(self, data):
        """
        The function takes all the arguments from the json (data) and puts them in the members of this class.
        :param data: a json file.
        :return: The function doesn't return a value.
        """
        obj = json.loads(data)
        self.command_id = obj['command_id']

    def handle(self, authenticated_sockets):
        """
        The function handles the request
        :param authenticated_sockets: A dictionary of all the users the logged in once.
        key: socket, value: username
        :return: The function handles getting all the chats from DB.
        """

        str_db = open('db.json', 'r').read()
        json_db = json.loads(str_db)

        # if the sender is not authenticated - return FAIL
        if self.sender_socket not in authenticated_sockets.keys():
            self.sender_socket.send(b'FAIL')
            return

        dict_chats = {}  # a dictionary with all the chats
        username = authenticated_sockets[self.sender_socket]
        for chat_name in json_db['chats'].keys():
            # If the username is one of the participants in the chat
            if username in json_db['chats'][chat_name]['chat_participants']:
                dict_chats[chat_name] = {'chat_participants': json_db['chats'][chat_name]['chat_participants'],
                                         'chat_type': json_db['chats'][chat_name]['chat_type'],
                                         'sender_username': username}

        bytes_dict_chats = json.dumps(dict_chats).encode()
        self.sender_socket.send(bytes_dict_chats)


