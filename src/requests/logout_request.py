from src.requests.message import Message
import json


class LogoutRequest(Message):
    def __init__(self):
        # TODO: init the parent
        self.command_id = 'LogoutRequest'
        self.username = None

    def pack(self):
        obj = {'command_id': self.command_id, 'username': self.username}
        return json.dumps(obj)

    def unpack(self, data):
        obj = json.loads(data)
        self.command_id = obj['command_id']
        self.username = obj['username']

    def handle(self, authenticated_sockets):
        str_db = open('db.json', 'r').read()
        json_db = json.loads(str_db)

        if self.sender_socket not in authenticated_sockets.keys():
            self.sender_socket.send(b'Please login first!')

        if self.username != authenticated_sockets[self.sender_socket]:
            self.sender_socket.send(b'Wrong username!')

        if self.username in json_db['users'].keys():
            json_db['users'][self.username]['is_connected'] = False
            str_modified_db = json.dumps(json_db)
            open('db.json', 'w').write(str_modified_db)

            self.sender_socket.send(b'SUCCESS')
            return

        self.sender_socket.send(b'FAIL')
