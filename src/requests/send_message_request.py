from src.requests.message import Message
import json
import datetime


class SendMessageRequest(Message):

    def __init__(self):
        """
        Constructor
        """
        super().__init__()
        self.command_id = 'SendMessageRequest'
        self.sender_username = None
        self.recipients = None
        self.type_of_message = None
        self.message_content = None
        self.group_name = None

    def pack(self):
        """
        The function doesn't get parameters.
        :return: The function returns a json with all the fields in the class SendMessageRequest.
        """
        obj = {'command_id': self.command_id,
               'username': self.sender_username,
               'recipients': self.recipients,
               'group_name': self.group_name,
               'type_of_message': self.type_of_message,
               'message_content': self.message_content}
        return json.dumps(obj)

    def unpack(self, data):
        """
        The function takes all the arguments from the json (data) and puts them in the members of this class.
        :param data: a json file.
        :return: The function doesn't return a value.
        """
        obj = json.loads(data)
        self.command_id = obj['command_id']
        self.sender_username = obj['username']
        self.recipients = obj['recipients']
        self.group_name = obj['group_name']
        self.type_of_message = obj['type_of_message']
        self.message_content = obj['message_content']

    def handle(self, authenticated_sockets):
        """
        The function handles the request
        :param authenticated_sockets: A dictionary of all the users the logged in once.
        key: socket, value: username
        :return: The function handles sending a message request.
        """
        # if the content of the message is empty - return FAIL
        if self.message_content == "":
            self.sender_socket.send(b'FAIL')
            return

        # if the sender is not authenticated - return FAIL
        if self.sender_socket not in authenticated_sockets.keys():
            self.sender_socket.send(b'FAIL')
            return

        str_db = open('db.json', 'r').read()
        json_db = json.loads(str_db)

        current_time_dict = get_current_time()  # a dictionary of the current time
        current_hour = current_time_dict['hour']  # the current hour
        current_minutes = current_time_dict['minutes']  # the current minutes
        string_current_time = str(current_hour) + ":" + str(current_minutes)  # the current time (string)

        # if the type of the message is PRIVATE
        if self.type_of_message == 'private':
            # A list of 2 people (one of them is the sender username and the other is the username of the recipient)
            recipients = self.recipients.split(',')

            # removing the username of the sender so the username of the recipient stays in the list
            recipients.remove(self.sender_username)
            recipient_username = recipients[0]

            # if the recipient doesn't exist in the DB but he's authenticated
            if recipient_username not in json_db['chats']:
                # Create a new chat in the DB
                json_db['chats'][self.recipients] = {}
                json_db['chats'][self.recipients]['chat_type'] = 'private'
                json_db['chats'][self.recipients]['chat_messages'] = []
                json_db['chats'][self.recipients]['chat_participants'] = self.recipients.split(',')

            # all the recipients in the chat now have a new chat
            for recipient in json_db['chats'][self.recipients]['chat_participants']:
                # Updating the field is_update to True
                json_db['users'][recipient]['is_update'] = True

            # Adding the message to the DB
            json_db['chats'][self.recipients]['chat_messages'].append({'message_content': self.message_content,
                                                                       'from': self.sender_username,
                                                                       'time': str(string_current_time)})

            str_modified_db = json.dumps(json_db)
            open('db.json', 'w').write(str_modified_db)
            self.sender_socket.send(b'SUCCESS')
            return

        # if the type of the message is GROUP
        elif self.type_of_message == 'group':
            # if the name of the group doesn't exist in the DB
            if self.group_name not in json_db['chats']:
                # Create a new chat in the DB
                json_db['chats'][self.group_name] = {}
                json_db['chats'][self.group_name]['chat_type'] = 'group'
                json_db['chats'][self.group_name]['chat_participants'] = self.recipients.split(',')
                json_db['chats'][self.group_name]['chat_messages'] = []

            # Adding the message to the DB
            json_db['chats'][self.group_name]['chat_messages'].append({'message_content': self.message_content,
                                                                       'from': self.sender_username,
                                                                       'time': str(string_current_time)})

            participants = json_db['chats'][self.group_name]['chat_participants']
            # all the recipients in the chat now have a new chat
            for recipient in participants:
                # Updating the field is_update to True
                json_db['users'][recipient]['is_update'] = True

            str_modified_db = json.dumps(json_db)
            open('db.json', 'w').write(str_modified_db)
            self.sender_socket.send(b'SUCCESS')
            return

        self.sender_socket.send(b'FAIL')


def get_current_time():
    """
    The function doesn't get parameters.
    :return: The function returns a dictionary of the current time (hours and minutes).
    """
    current_time = datetime.datetime.now()
    current_time_dict = {'hour': current_time.hour,
                         'minutes': current_time.minute}
    return current_time_dict
