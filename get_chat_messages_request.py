from message import Message
import json
import time
import hashlib


class GetChatMessagesRequest(Message):
    def __init__(self):
        # TODO: init the parent
        self.command_id = 'GetChatMessagesRequest'
        self.chat_name = None

    def pack(self):
        obj = {'command_id': self.command_id, 'chat_name': self.chat_name}
        return json.dumps(obj)

    def unpack(self, data):
        obj = json.loads(data)
        self.command_id = obj['command_id']
        self.chat_name = obj['chat_name']

    def handle(self, authenticated_sockets):
        print("trying to handle - message")
        str_db = open('db.json', 'r').read()
        json_db = json.loads(str_db)

        if self.sender_socket not in authenticated_sockets.keys():
            self.sender_socket.send(b'Please login first!')

        username = authenticated_sockets[self.sender_socket]
        if self.chat_name not in json_db['chats']:
            self.sender_socket.send(b'FAIL')
            return
        if username not in json_db['chats'][self.chat_name]['chat_participants']:
            self.sender_socket.send(b'FAIL')
            return
        list_messages = json_db['chats'][self.chat_name]['chat_messages']
        dict_messages = {'username': username, 'list_messages': list_messages}
        bytes_dict_messages = json.dumps(dict_messages).encode()
        self.sender_socket.send(bytes_dict_messages)