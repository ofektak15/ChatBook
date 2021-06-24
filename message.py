import json


class Message(object):
    def __init__(self):
        self.command_id = None
        self.username = None
        self.socket = None

    def pack(self):
        raise NotImplementedError

    def unpack(self, data):
        raise NotImplementedError

    def handle(self, authenticated_sockets):
        raise NotImplementedError


class SendMessageRequest(Message):
    TYPE_BROADCAST = 'BROADCAST_MESSAGE'
    TYPE_PRIVATE = 'PRIVATE_MESSAGE'

    def __init__(self):
        # TODO: init the parent
        self.command_id = 'SendMessageRequest'
        self.username = None
        self.recipient = None
        self.type_of_message = None
        self.message_content = None

    def pack(self):
        obj = {'command_id': self.command_id, 'username': self.username, 'recipient': self.recipient,
               'type_of_message': self.type_of_message, 'message_content': self.message_content}
        return json.dumps(obj)

    def unpack(self, data):
        obj = json.loads(data)
        self.command_id = obj['command_id']
        self.username = obj['username']
        self.recipient = obj['recipient']
        self.type_of_message = obj['type_of_message']
        self.message_content = obj['message_content']

    def handle(self, authenticated_sockets):
        if self.socket not in authenticated_sockets.keys():
            self.socket.send('Please login first!')

        for socket, username in authenticated_sockets.items():
            if username == self.recipient:
                socket.send(self.pack().encode())
                self.socket.send(b'SUCCESS')
                return

        self.socket.send(b'FAIL')


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
            if self.password == json_db['users'][self.username]:
                authenticated_sockets[self.socket] = self.username
                self.socket.send(b'SUCCESS')
                return
        # DB
        # SOCKET OF LOGGED USERS
        self.socket.send(b'FAIL')


class RegisterRequest(Message):
    def __init__(self):
        # TODO: init the parent
        self.command_id = 'RegisterRequest'
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
            self.socket.send(b'FAIL')
            return

        json_db['users'][self.username] = self.password
        str_modified_db = json.dumps(json_db)
        open('db.json', 'w').write(str_modified_db)

        self.socket.send(b'SUCCESS')


MESSAGES = {'SendMessageRequest': SendMessageRequest, 'LoginRequest': LoginRequest, 'RegisterRequest': RegisterRequest}
