from src.requests.message import Message
import json
import time
import hashlib


class LoginRequest(Message):
    def __init__(self):
        # TODO: init the parent
        self.command_id = 'LoginRequest'
        self.username = None
        self.password = None

    def pack(self):
        obj = {'command_id': self.command_id, 'username': self.username, 'password': self.password}
        return json.dumps(obj)

    def unpack(self, data):
        obj = json.loads(data)
        self.command_id = obj['command_id']
        self.username = obj['username']
        self.password = obj['password']

    def handle(self, authenticated_sockets):
        str_db = open('db.json', 'r').read()
        json_db = json.loads(str_db)

        if self.username in json_db['users'].keys():
            hashed_password = hashlib.md5(self.password.encode()).hexdigest()
            if hashed_password == json_db['users'][self.username]['password']:
                authenticated_sockets[self.sender_socket] = self.username
                if not json_db['users'][self.username]['is_connected']:
                    json_db['users'][self.username]['is_connected'] = True
                    str_modified_db = json.dumps(json_db)
                    open('db.json', 'w').write(str_modified_db)
                    self.sender_socket.send(b'SUCCESS')
                    return

        self.sender_socket.send(b'FAIL')
