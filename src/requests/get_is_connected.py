from src.requests.message import Message
import json
import time
import hashlib


class GetIsConnected(Message):
    def __init__(self):
        self.command_id = 'GetIsConnected'
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

        if json_db['users'][self.username]['is_connected']:
            return True
        else:
            return False
