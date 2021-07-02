from src.requests.message import Message
import json
import datetime


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
                current_time_dict = get_current_time()
                current_hour = current_time_dict['hour']
                current_minutes = current_time_dict['minutes']
                string_current_time = str(current_hour) + ":" + str(current_minutes)

                dict_chats[chat_name] = {'chat_participants': json_db['chats'][chat_name]['chat_participants'],
                                         'chat_type': json_db['chats'][chat_name]['chat_type'],
                                         'sender_username': username,
                                         'time': string_current_time}

        bytes_dict_chats = json.dumps(dict_chats).encode()
        self.sender_socket.send(bytes_dict_chats)


def get_current_time():
    current_time = datetime.datetime.now()
    current_time_dict = {'hour': current_time.hour,
                         'minutes': current_time.minute}
    return current_time_dict
