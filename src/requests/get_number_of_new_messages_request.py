from src.requests.message import Message
import json


class GetNumberOfNewMessages(Message):
    def __init__(self):
        """
        Constructor
        """
        super().__init__()
        self.command_id = 'GetNumberOfNewMessages'
        self.username = None
        self.chat_name = None

    def pack(self):
        """
        The function doesn't get parameters.
        :return: The function returns a json with all the fields in the class GetUsernameRequest.
        """
        obj = {'command_id': self.command_id, 'username': self.username, 'chat_name': self.chat_name}
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
        self.chat_name = obj['chat_name']

    def handle(self, authenticated_sockets):
        """
        The function handles the request
        :param authenticated_sockets: A dictionary of all the users the logged in once.
        key: socket, value: username
        :return: The function handles getting a username.
        """

        # if the sender is not authenticated - return FAIL
        if self.sender_socket not in authenticated_sockets.keys():
            self.sender_socket.send(b'FAIL')
            return

        str_db = open('db.json', 'r').read()
        json_db = json.loads(str_db)

        number_of_new_messages = json_db['chats'][self.chat_name]['unread_messages'][self.username]
        number_of_new_messages = str(number_of_new_messages)

        self.sender_socket.send(number_of_new_messages.encode())
