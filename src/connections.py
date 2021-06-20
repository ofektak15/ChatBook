class Connections(object):
    def __init__(self):
        self.connections = {}

    def add(self, connection):
        self.connections[connection.sock] = connection

    def remove(self, connection):
        self.connections.pop(connection.sock)

    def get_connections(self):
        return self.connections.values()

    def get_socks(self):
        return self.connections.keys()

    def get(self, sock):
        return self.connections[sock]
