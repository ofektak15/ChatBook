from serializer import Serializer


class ProtoLogin(Serializer):
    def __init__(self, username, password):
        self.username = username
        self.password = password


class ProtoBroadcast(Serializer):
    def __init__(self, origin, content):
        self.origin = origin
        self.content = content
