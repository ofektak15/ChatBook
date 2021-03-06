import socket
from threading import Thread

from const import Consts
from protocol import ProtoLogin, ProtoBroadcast


class Client(object):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.username = ''
        self.password = ''

    def start(self):
        self.connect()

        self.authenticate()

        thread_recv = Thread(target=self._handle_recv)
        thread_recv.start()

        thread_send = Thread(target=self._handle_send)
        thread_send.start()

        thread_send.join()

    def connect(self):
        self.client.connect((self.ip, self.port))

    def _handle_send(self):
        while True:
            content = input('>>> ')
            proto_broadcast = ProtoBroadcast(origin=self.username, content=content)
            data = proto_broadcast.to_json()
            msg = data.encode()
            self.client.send(msg)

    def _handle_recv(self):
        while True:
            msg = self.client.recv(Consts.MAX_MSG_LENGTH)
            data = msg.decode()
            print(data)

    def authenticate(self):
        while True:
            self.username = input('Enter username: ')
            self.password = input('Enter password: ')
            proto_login = ProtoLogin(self.username, self.password)
            data = proto_login.to_json()
            msg = data.encode()
            self.client.send(msg)
            # TODO: refactor
            code = self.client.recv(Consts.AUTHENTICATED_STATUS_MSG_LENGTH)
            if code == b'1':
                break
            print('Please try again...')
        print('Authenticated successfully!!!')
