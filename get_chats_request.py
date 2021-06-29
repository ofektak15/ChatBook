from message import Message
import json
import time
import hashlib


class GetChatsRequest(Message):
    def __init__(self):
        # TODO: init the parent
        self.command_id = 'GetChatsRequest'

    def pack(self):
        obj = {'command_id': self.command_id}
        return json.dumps(obj)

    def unpack(self, data):
        obj = json.loads(data)
        self.command_id = obj['command_id']

    def handle(self, authenticated_sockets):
        str_db = open('db.json', 'r').read()
        json_db = json.loads(str_db)

        if self.sender_socket not in authenticated_sockets.keys():
            self.sender_socket.send(b'Please login first!')

        dict_chats = {}
        username = authenticated_sockets[self.sender_socket]
        for chat_name in json_db['chats'].keys():
            if username in json_db['chats'][chat_name]['chat_participants']:
                dict_chats[chat_name] = {'chat_participants': json_db['chats'][chat_name]['chat_participants'],
                                         'chat_type': json_db['chats'][chat_name]['chat_type'],
                                         'sender_username': username}

        bytes_dict_chats = json.dumps(dict_chats).encode()
        self.sender_socket.send(bytes_dict_chats)