import socket

from const import Consts


class Connection(object):
    def __init__(self, sock):
        self.sock = sock

    def is_closed(self):
        data = self.sock.recv(16, socket.MSG_DONTWAIT | socket.MSG_PEEK)
        if len(data) == 0:
            self.sock.close()

    def send(self, msg):
        self.sock.send(msg)

    def recv(self, size=Consts.MAX_MSG_LENGTH):
        self.sock.recv(size)

    def close(self):
        self.sock.close()
