from src.requests.message import Message
import json
import time
import hashlib


class SendMessageRequest(Message):
    TYPE_BROADCAST = 'BROADCAST_MESSAGE'
    TYPE_PRIVATE = 'PRIVATE_MESSAGE'

    def __init__(self):
        # TODO: init the parent
        self.command_id = 'SendMessageRequest'
        self.sender_username = None
        self.recipients = None
        self.type_of_message = None
        self.message_content = None
        self.group_name = None

    def pack(self):
        obj = {'command_id': self.command_id,
               'username': self.sender_username,
               'recipients': self.recipients,
               'group_name': self.group_name,
               'type_of_message': self.type_of_message,
               'message_content': self.message_content}
        return json.dumps(obj)

    def unpack(self, data):
        obj = json.loads(data)
        self.command_id = obj['command_id']
        self.sender_username = obj['username']
        self.recipients = obj['recipients']
        self.group_name = obj['group_name']
        self.type_of_message = obj['type_of_message']
        self.message_content = obj['message_content']

    def handle(self, authenticated_sockets):
        str_db = open('db.json', 'r').read()
        json_db = json.loads(str_db)

        if self.sender_socket not in authenticated_sockets.keys():
            self.sender_socket.send(b'Please login first!')

        if self.sender_username != authenticated_sockets[self.sender_socket]:
            self.sender_socket.send(b'Wrong username!')

        if self.type_of_message == 'private':
            recipients = self.recipients.split(',')  # ['ofek', 'tomer']
            recipients.remove(self.sender_username)
            recipient_username = recipients[0]
            if self.recipients not in json_db['chats']:
                json_db['chats'][self.recipients] = {}
                json_db['chats'][self.recipients]['chat_type'] = 'private'
                json_db['chats'][self.recipients]['chat_messages'] = []
                json_db['chats'][self.recipients]['chat_participants'] = self.recipients.split(',')

            json_db['chats'][self.recipients]['chat_messages'].append({'message_content': self.message_content,
                                                                       'from': self.sender_username,
                                                                       'time': str(time.time()),
                                                                       'received': [self.sender_username]})

            for socket, username in authenticated_sockets.items():
                if username == recipient_username:
                    socket.send(self.pack().encode())
                    json_db['chats'][self.recipients]['chat_messages'][-1]['received'].append(username)

            str_modified_db = json.dumps(json_db)
            open('db.json', 'w').write(str_modified_db)
            self.sender_socket.send(b'SUCCESS')
            return

        elif self.type_of_message == 'group':
            if self.group_name not in json_db['chats']:
                json_db['chats'][self.group_name] = {}
                json_db['chats'][self.group_name]['chat_type'] = 'group'
                json_db['chats'][self.group_name]['chat_participants'] = self.recipients.split(',')
                json_db['chats'][self.group_name]['chat_messages'] = []

            json_db['chats'][self.group_name]['chat_messages'].append({'message_content': self.message_content,
                                                                       'from': self.sender_username,
                                                                       'time': str(time.time()),
                                                                       'received': [self.sender_username]})

            list_from_db = json_db['chats'][self.group_name]['chat_participants']
            true_recipients = list(list_from_db)
            true_recipients.remove(self.sender_username)

            for socket, username in authenticated_sockets.items():
                if username in true_recipients:
                    # socket.send(self.pack().encode())
                    json_db['chats'][self.group_name]['chat_messages'][-1]['received'].append(username)

            str_modified_db = json.dumps(json_db)
            open('db.json', 'w').write(str_modified_db)
            self.sender_socket.send(b'SUCCESS')
            return

        self.sender_socket.send(b'FAIL')
