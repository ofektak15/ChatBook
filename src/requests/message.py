class Message(object):
    def __init__(self):
        self.command_id = None
        self.sender_socket = None

    def pack(self):
        """
        Virtual function
        """
        raise NotImplementedError

    def unpack(self, data):
        """
        Virtual function
        """
        raise NotImplementedError

    def handle(self, authenticated_sockets):
        """
        Virtual function
        """
        raise NotImplementedError
