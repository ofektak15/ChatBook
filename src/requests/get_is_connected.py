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
        if self.sender_socket not in authenticated_sockets.keys():
            self.sender_socket.send(b'Please login first!')

        is_connected = False
        if json_db['users'][self.username]:
            is_connected = json_db['users'][self.username]['is_connected']

        dict_messages = {'is_connected': is_connected}
        bytes_dict_messages = json.dumps(dict_messages).encode()
        self.sender_socket.send(bytes_dict_messages)
