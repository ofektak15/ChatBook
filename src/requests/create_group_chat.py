from src.requests.message import Message
import json


class CreateGroupChat(Message):
    def __init__(self):
        """
        Constructor
        """
        super().__init__()
        self.command_id = 'CreateGroupChat'
        self.recipient = None
        self.group_name = None

    def pack(self):
        """
        The function doesn't get parameters.
        :return: The function returns a json with all the fields in the class CreateGroupChat.
        """
        obj = {'command_id': self.command_id, 'recipient': self.recipient, 'group_name': self.group_name}
        return json.dumps(obj)

    def unpack(self, data):
        """
        The function takes all the arguments from the json (data) and puts them in the members of this class.
        :param data: a json file.
        :return: The function doesn't return a value.
        """
        obj = json.loads(data)
        self.command_id = obj['command_id']
        self.recipient = obj['recipient']
        self.group_name = obj['group_name']

    def handle(self, authenticated_sockets):
        """
        The function handles the request
        :param authenticated_sockets: A dictionary of all the users the logged in once.
        key: socket, value: username
        :return: The function handles creating a group chat.
        """
        str_db = open('db.json', 'r').read()
        json_db = json.loads(str_db)

        recipients = self.recipient.split(',')  # the participants in the group
        for username in recipients:
            # if one of the participant's username doesn't exist in the DB - return FAIL
            if username not in json_db['users'].keys():
                self.sender_socket.send(b'FAIL')
                return

        # if the sender is not authenticated - return FAIL
        if self.sender_socket not in authenticated_sockets.keys():
            self.sender_socket.send(b'FAIL')
            return

        # Creating a new group chat in DB
        username = authenticated_sockets[self.sender_socket]
        chat_name = self.group_name
        json_db['chats'][chat_name] = {}
        json_db['chats'][chat_name]['chat_type'] = "group"
        json_db['chats'][chat_name]['chat_participants'] = recipients + [username]
        json_db['chats'][chat_name]['chat_messages'] = []
        json_db['chats'][chat_name]['unread_messages'] = {}
        for participant in json_db['chats'][chat_name]['chat_participants']:
            json_db['chats'][chat_name]['unread_messages'][participant] = 0

        # all the recipients in the chat now have a new chat
        for recipient in json_db['chats'][chat_name]['chat_participants']:
            # Updating the field is_update to True
            json_db['users'][recipient]['is_update'] = True

        str_modified_db = json.dumps(json_db)
        open('db.json', 'w').write(str_modified_db)

        self.sender_socket.send(b'SUCCESS')
