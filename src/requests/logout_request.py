from src.requests.message import Message
import json


class LogoutRequest(Message):
    def __init__(self):
        """
        Constructor
        """
        super().__init__()
        self.command_id = 'LogoutRequest'
        self.username = None

    def pack(self):
        """
        The function doesn't get parameters.
        :return: The function returns a json with all the fields in the class LogoutRequest.
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
        :return: The function handles logging out.
        """

        str_db = open('db.json', 'r').read()
        json_db = json.loads(str_db)

        # if the sender is not authenticated - return FAIL
        if self.sender_socket not in authenticated_sockets.keys():
            self.sender_socket.send(b'FAIL')

        # if the username exists
        if self.username in json_db['users'].keys():
            # changing from connected to disconnected
            json_db['users'][self.username]['is_connected'] = False

            str_modified_db = json.dumps(json_db)
            open('db.json', 'w').write(str_modified_db)

            self.sender_socket.send(b'SUCCESS')
            return

        self.sender_socket.send(b'FAIL')
