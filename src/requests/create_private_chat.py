from src.requests.message import Message
import json


class CreatePrivateChat(Message):
    def __init__(self, recipient):
        # TODO: init the parent
        self.command_id = 'CreatePrivateChat'
        self.recipient = recipient

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

        json_db['users'][self.recipient] = {}
        json_db['users'][self.recipient]['chat_type'] = "private"
        json_db['users'][self.recipient]['chat_participants'] = [self.sender_username, self.recipient]

        str_modified_db = json.dumps(json_db)
        open('db.json', 'w').write(str_modified_db)

        self.sender_socket.send(b'SUCCESS')

    def is_user_exist(self):
        str_db = open('db.json', 'r').read()
        json_db = json.loads(str_db)

        for username in json_db['chats']:
            if self.recipient == username:
                return True

        return False
