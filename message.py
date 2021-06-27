import json
import time
import hashlib


class Message(object):
    def __init__(self):
        self.command_id = None
        self.sender_username = None
        self.sender_socket = None

    def pack(self):
        raise NotImplementedError

    def unpack(self, data):
        raise NotImplementedError

    def handle(self, authenticated_sockets):
        raise NotImplementedError


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
               'recpients': self.recipients,
               'group_name': self.group_name,
               'type_of_message': self.type_of_message,
               'message_content': self.message_content}
        return json.dumps(obj)

    def unpack(self, data):
        obj = json.loads(data)
        self.command_id = obj['command_id']
        self.sender_username = obj['username']
        self.recipients = obj['recpients']
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
                json_db['chats'][self.recipients]['participants'] = self.recipients.split(',')

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
                json_db['chats'][self.recipients]['chat_type'] = 'group'
                json_db['chats'][self.recipients]['participants'] = self.recipients.split(',')
                json_db['chats'][self.recipients]['chat_messages'] = []

            json_db['chats'][self.group_name]['chat_messages'].append({'message_content': self.message_content,
                                                                       'from': self.sender_username,
                                                                       'time': str(time.time()),
                                                                       'received': [self.sender_username]})

            true_recipients = self.recipients.split(',').remove(self.sender_username)
            for socket, username in authenticated_sockets.items():
                if username in true_recipients:
                    socket.send(self.pack().encode())
                    json_db['chats'][self.group_name]['chat_messages'][-1]['received'].append(username)

            str_modified_db = json.dumps(json_db)
            open('db.json', 'w').write(str_modified_db)
            self.sender_socket.send(b'SUCCESS')
            return

        self.sender_socket.send(b'FAIL')


class LoginRequest(Message):
    def __init__(self):
        # TODO: init the parent
        self.command_id = 'LoginRequest'
        self.username = None
        self.password = None

    def pack(self):
        obj = {'command_id': self.command_id, 'username': self.username, 'password': self.password}
        return json.dumps(obj)

    def unpack(self, data):
        obj = json.loads(data)
        self.command_id = obj['command_id']
        self.username = obj['username']
        self.password = obj['password']

    def handle(self, authenticated_sockets):
        str_db = open('db.json', 'r').read()
        json_db = json.loads(str_db)

        if self.username in json_db['users'].keys():

            hashed_password = hashlib.md5(self.password.encode()).hexdigest()
            if hashed_password == json_db['users'][self.username]['password']:
                authenticated_sockets[self.sender_socket] = self.username
                json_db['users'][self.username]['is_connected'] = True
                str_modified_db = json.dumps(json_db)
                open('db.json', 'w').write(str_modified_db)
                self.sender_socket.send(b'SUCCESS')
                return
        # DB
        # SOCKET OF LOGGED USERS
        self.sender_socket.send(b'FAIL')


class LogoutRequest(Message):
    def __init__(self):
        # TODO: init the parent
        self.command_id = 'LogoutRequest'
        self.username = None
        self.password = None

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
            self.sender_socket.send('Please login first!')

        if self.sender_username != authenticated_sockets[self.sender_socket]:
            self.sender_socket.send('Wrong username!')

        if self.username in json_db['users'].keys():
            json_db['users'][self.username]['is_connected'] = False
            str_modified_db = json.dumps(json_db)
            open('db.json', 'w').write(str_modified_db)
            self.sender_socket.send(b'SUCCESS')
            return

        self.sender_socket.send(b'FAIL')


class RegisterRequest(Message):
    def __init__(self):
        # TODO: init the parent
        self.command_id = 'RegisterRequest'
        self.username = None
        self.password = None

    def pack(self):
        obj = {'command_id': self.command_id, 'username': self.username, 'password': self.password}
        return json.dumps(obj)

    def unpack(self, data):
        obj = json.loads(data)
        self.command_id = obj['command_id']
        self.username = obj['username']
        self.password = obj['password']

    def handle(self, authenticated_sockets):
        str_db = open('db.json', 'r').read()
        json_db = json.loads(str_db)

        if self.username in json_db['users'].keys():
            self.sender_socket.send(b'FAIL')
            return

        json_db['users'][self.username] = {}
        hashed_password = hashlib.md5(self.password.encode()).hexdigest()
        json_db['users'][self.username]['password'] = hashed_password
        json_db['users'][self.username]['is_connected'] = False
        str_modified_db = json.dumps(json_db)
        open('db.json', 'w').write(str_modified_db)

        self.sender_socket.send(b'SUCCESS')


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

        list_chat_names = []
        username = authenticated_sockets[self.sender_socket]
        for chat_name in json_db['chats'].keys():
            if username in json_db['chats'][chat_name]['chat_participants']:
                if json_db['chats'][chat_name]['chat_type'] == 'private':
                    recipients = chat_name.split(',')  # ['ofek', 'tomer']
                    recipients.remove(username)
                    real_chat_name = recipients[0]
                    list_chat_names.append(real_chat_name)
                else:  # group
                    list_chat_names.append(chat_name)

        bytes_list_chat_names = json.dumps(list_chat_names).encode()
        self.sender_socket.send(bytes_list_chat_names)


MESSAGES = {'GetChatsRequest': GetChatsRequest, 'LogoutRequest': LogoutRequest,
            'SendMessageRequest': SendMessageRequest, 'LoginRequest': LoginRequest,
            'RegisterRequest': RegisterRequest}
