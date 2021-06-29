from src.requests.message import Message
import json
import time
import hashlib


class GetUsernameRequest(Message):
    def __init__(self):
        self.command_id = 'GetUsernameRequest'
        self.username = None

    def pack(self):
        obj = {'command_id': self.command_id, 'username': self.username}
        return json.dumps(obj)

    def unpack(self, data):
        obj = json.loads(data)
        self.command_id = obj['command_id']
        self.username = obj['username']

    def handle(self, authenticated_sockets):
        self.sender_socket.send(self.username)
