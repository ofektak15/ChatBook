from src.requests.message import Message
import json


class CreatePrivateChat(Message):
    def __init__(self):
        # TODO: init the parent
        self.command_id = 'CreatePrivateChat'
        self.recipient = None

    def pack(self):
        obj = {'command_id': self.command_id, 'recipient': self.recipient}
        return json.dumps(obj)

    def unpack(self, data):
        obj = json.loads(data)
        self.command_id = obj['command_id']
        self.recipient = obj['recipient']

    def handle(self, authenticated_sockets):
        str_db = open('db.json', 'r').read()
        json_db = json.loads(str_db)

        if not self.is_user_exist():
            self.sender_socket.send(b'FAIL')
            return

        if self.sender_socket not in authenticated_sockets.keys():
            self.sender_socket.send(b'Please login first!')

        username = authenticated_sockets[self.sender_socket]

        chat_name = '{},{}'.format(self.recipient, username)
        json_db['chats'][chat_name] = {}
        json_db['chats'][chat_name]['chat_type'] = "private"
        json_db['chats'][chat_name]['chat_participants'] = [username, self.recipient]
        json_db['chats'][chat_name]['chat_messages'] = []

        str_modified_db = json.dumps(json_db)
        open('db.json', 'w').write(str_modified_db)

        self.sender_socket.send(b'SUCCESS')

    def is_user_exist(self):
        str_db = open('db.json', 'r').read()
        json_db = json.loads(str_db)

        for username in json_db['users'].keys():
            if self.recipient == username:
                return True

        return False
