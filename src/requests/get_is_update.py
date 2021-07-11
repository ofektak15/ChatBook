from src.requests.message import Message
import json


class GetIsUpdate(Message):
    def __init__(self):
        """
        Constructor
        """
        super().__init__()
        self.command_id = 'GetIsUpdate'

    def pack(self):
        """
        The function doesn't get parameters.
        :return: The function returns a json with all the fields in the class GetIsUpdate.
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
        :return: The function handles getting if a username is connected or not.
        """

        str_db = open('db.json', 'r').read()
        json_db = json.loads(str_db)

        username = authenticated_sockets[self.sender_socket]
        is_update = json_db['users'][username]['is_update']  # if the username needs to be updated or not
        if is_update:
            json_db['users'][username]['is_update'] = False
            str_modified_db = json.dumps(json_db)
            open('db.json', 'w').write(str_modified_db)

        dict_messages = {'is_update': is_update}
        bytes_dict_messages = json.dumps(dict_messages).encode()
        self.sender_socket.send(bytes_dict_messages)
