from src.requests.message import Message
import json


class GetIsUpdate(Message):
    def __init__(self):
        # TODO: init the parent
        self.command_id = 'GetIsUpdate'

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
        username = authenticated_sockets[self.sender_socket]
        is_update = json_db['users'][username]['is_update']
        if is_update:
            json_db['users'][username]['is_update'] = False
            str_modified_db = json.dumps(json_db)
            open('db.json', 'w').write(str_modified_db)

        dict_messages = {'is_update': is_update}
        bytes_dict_messages = json.dumps(dict_messages).encode()
        self.sender_socket.send(bytes_dict_messages)
