from src.requests.message import Message
import json


class CreateGroupChat(Message):
    def __init__(self):
        # TODO: init the parent
        self.command_id = 'CreateGroupChat'
        self.recipient = None
        self.group_name = None

    def pack(self):
        obj = {'command_id': self.command_id, 'recipient': self.recipient, 'group_name': self.group_name}
        return json.dumps(obj)

    def unpack(self, data):
        obj = json.loads(data)
        self.command_id = obj['command_id']
        self.recipient = obj['recipient']
        self.group_name = obj['group_name']

    def handle(self, authenticated_sockets):
        str_db = open('db.json', 'r').read()
        json_db = json.loads(str_db)

        recipients = self.recipient.split(',')
        for username in recipients:
            if username not in json_db['users'].keys():
                self.sender_socket.send(b'FAIL')
                return

        if self.sender_socket not in authenticated_sockets.keys():
            self.sender_socket.send(b'Please login first!')

        username = authenticated_sockets[self.sender_socket]
        print("username:" + username)
        chat_name = self.group_name
        json_db['chats'][chat_name] = {}
        json_db['chats'][chat_name]['chat_type'] = "group"
        json_db['chats'][chat_name]['chat_participants'] = recipients + [username]
        json_db['chats'][chat_name]['chat_messages'] = []

        for recipient in json_db['chats'][chat_name]['chat_participants']:
            json_db['users'][recipient]['is_update'] = True

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
