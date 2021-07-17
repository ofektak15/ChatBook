from src.requests.message import Message
import json


class GetChatMessagesRequest(Message):
    def __init__(self):
        """
        Constructor
        """
        super().__init__()
        self.command_id = 'GetChatMessagesRequest'
        self.chat_name = None
        self.reset_unread_msgs_count = None

    def pack(self):
        """
        The function doesn't get parameters.
        :return: The function returns a json with all the fields in the class GetChatMessagesRequest.
        """
        obj = {'command_id': self.command_id, 'chat_name': self.chat_name, 'reset_unread_msgs_count': self.reset_unread_msgs_count}
        return json.dumps(obj)

    def unpack(self, data):
        """
        The function takes all the arguments from the json (data) and puts them in the members of this class.
        :param data: a json file.
        :return: The function doesn't return a value.
        """
        obj = json.loads(data)
        self.command_id = obj['command_id']
        self.chat_name = obj['chat_name']
        self.reset_unread_msgs_count = obj['reset_unread_msgs_count']

    def handle(self, authenticated_sockets):
        """
        The function handles the request
        :param authenticated_sockets: A dictionary of all the users the logged in once.
        key: socket, value: username
        :return: The function handles getting messages from a specific chat.
        """

        str_db = open('db.json', 'r').read()
        json_db = json.loads(str_db)

        # if the sender is not authenticated - return FAIL
        if self.sender_socket not in authenticated_sockets.keys():
            self.sender_socket.send(b'FAIL')
            return

        sender_username = authenticated_sockets[self.sender_socket]

        # If the name of the chat doesn't exist in the DB - return FAIL
        if self.chat_name not in json_db['chats']:
            self.sender_socket.send(b'FAIL')
            return

        # If the username is not one of the participants in the chat - return FAIL
        if sender_username not in json_db['chats'][self.chat_name]['chat_participants']:
            self.sender_socket.send(b'FAIL')
            return

        if self.reset_unread_msgs_count == "True":
            # PRIVATE CHAT
            if ',' in self.chat_name:
                participants_string = self.chat_name
                participants_list = participants_string.split(',')
                participants_list.remove(sender_username)  # now only the recipient is in the list

                # when the user enters to a chat - he doesn't have new messages there
                json_db['chats'][self.chat_name]['unread_messages'][participants_list[0]] = 0

            # GROUP CHAT
            else:
                participants_list = json_db['chats'][self.chat_name]['chat_participants']
                participants_list.remove(sender_username)  # now only the recipients are in the list

                for participant in participants_list:
                    # when the user enters to a chat - he doesn't have new messages there
                    json_db['chats'][self.chat_name]['unread_messages'][participant] = 0

        list_messages = json_db['chats'][self.chat_name]['chat_messages']  # list of messages
        dict_messages = {'username': sender_username, 'list_messages': list_messages}  # dictionary of the messages
        bytes_dict_messages = json.dumps(dict_messages).encode()

        # updating the DB
        str_modified_db = json.dumps(json_db)
        open('db.json', 'w').write(str_modified_db)

        self.sender_socket.send(bytes_dict_messages)  # sending a dictionary of messages
