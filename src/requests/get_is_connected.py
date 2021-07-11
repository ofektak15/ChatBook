from src.requests.message import Message
import json


class GetIsConnected(Message):
    def __init__(self):
        """
        Constructor
        """
        super().__init__()
        self.command_id = 'GetIsConnected'
        self.username = None

    def pack(self):
        """
        The function doesn't get parameters.
        :return: The function returns a json with all the fields in the class GetIsConnected.
        """
        obj = {'command_id': self.command_id, 'username': self.username}
        return json.dumps(obj)

    def unpack(self, data):
        """
        The function takes all the arguments from the json (data) and puts them in the members of this class.
        :param data: a json file.
        :return: The function doesn't return a value.
        """
        obj = json.loads(data)
        self.command_id = obj['command_id']
        self.username = obj['username']

    def handle(self, authenticated_sockets):
        """
        The function handles the request
        :param authenticated_sockets: A dictionary of all the users the logged in once.
        key: socket, value: username
        :return: The function handles getting if a username is connected or not.
        """

        str_db = open('db.json', 'r').read()
        json_db = json.loads(str_db)

        # if the sender is not authenticated - return FAIL
        if self.sender_socket not in authenticated_sockets.keys():
            self.sender_socket.send(b'FAIL')

        is_connected = json_db['users'][self.username]['is_connected']

        dict_messages = {'is_connected': is_connected}
        bytes_dict_messages = json.dumps(dict_messages).encode()
        self.sender_socket.send(bytes_dict_messages)
