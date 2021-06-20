from serializer import Serializer


class ProtoLogin(Serializer):
    def __init__(self, username, password):
        self.username = username
        self.password = password
