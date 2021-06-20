class ProtoLogin(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def serialize(self):
        return MAGIC

    def deserilze(self, s):
        return ProtoLogin
    # MAGIC = "{'username': 'USER', 'password': 'PASSWORD'}"
