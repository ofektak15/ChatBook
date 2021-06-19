import socket
from threading import Thread

from const import Consts


class Client(object):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def start(self):
        self.connect()

        thread_recv = Thread(target=self._handle_recv)
        thread_recv.start()

        thread_send = Thread(target=self._handle_send)
        thread_send.start()

        thread_send.join()

    def connect(self):
        self.client.connect((self.ip, self.port))

    def _handle_send(self):
        while True:
            data = input('>>> ')
            msg = data.encode()
            self.client.send(msg)

    def _handle_recv(self):
        while True:
            msg = self.client.recv(Consts.MAX_MSG_LENGTH)
            data = msg.decode()
            print(data)
