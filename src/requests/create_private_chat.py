from src.requests.message import Message
import json


class CreatePrivateChat(Message):
    def __init__(self):
        """
        Constructor
        """
        super().__init__()
        self.command_id = 'CreatePrivateChat'
        self.recipient = None

    def pack(self):
        """
        The function doesn't get parameters.
        :return: The function returns a json with all the fields in the class CreatePrivateChat.
        """
        obj = {'command_id': self.command_id, 'recipient': self.recipient}
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

    def handle(self, authenticated_sockets):
        """
        The function handles the request
        :param authenticated_sockets: A dictionary of all the users the logged in once.
        key: socket, value: username
        :return: The function handles creating a private chat.
        """

        str_db = open('db.json', 'r').read()
        json_db = json.loads(str_db)

        # If the recipient doesn't exist in the DB - return FAIL
        if not self.is_user_exist():
            self.sender_socket.send(b'FAIL')
            return

        # if the sender is not authenticated - return FAIL
        if self.sender_socket not in authenticated_sockets.keys():
            self.sender_socket.send(b'FAIL')
            return

        username = authenticated_sockets[self.sender_socket]

        # Creating a new private chat in DB
        chat_name = '{},{}'.format(self.recipient, username)
        json_db['chats'][chat_name] = {}
        json_db['chats'][chat_name]['chat_type'] = "private"
        json_db['chats'][chat_name]['chat_participants'] = [username, self.recipient]
        json_db['chats'][chat_name]['chat_messages'] = []

        # all the recipients in the chat now have a new chat
        for recipient in json_db['chats'][chat_name]['chat_participants']:
            # Updating the field is_update to True
            json_db['users'][recipient]['is_update'] = True

        str_modified_db = json.dumps(json_db)
        open('db.json', 'w').write(str_modified_db)

        self.sender_socket.send(b'SUCCESS')

    def is_user_exist(self):
        """
        The function doesn't get parameters.
        :return: The function returns true if the recipient exists in the DB. Else - returns false.
        """
        str_db = open('db.json', 'r').read()
        json_db = json.loads(str_db)

        for username in json_db['users'].keys():
            if self.recipient == username:
                return True

        return False
