import select
import socket
from threading import Thread

from connection import Connection
from const import Consts


class Server(object):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.connections = {}
        # [1,2,3,4,5,6,7,8,9,10] (O(n))
        # {'1': 1, ... , '9': 9 } (O(1))

    def start(self):
        self.server.bind((self.ip, self.port))
        self.server.listen(Consts.MAX_SERVER_LISTEN)

        thread_accept = Thread(target=self._handle_accept)
        thread_accept.start()

        thread_data = Thread(target=self._handle_data)
        thread_data.start()

        thread_manage = Thread(target=self._handle_manage)
        thread_manage.start()

        thread_manage.join()

        print('Exit unimplemented')
        exit(1)

    def _broadcast(self, msg, origin):
        socks = list(self.connections.keys())
        for sock in socks:
            if sock == origin:
                continue
            sock.send(msg)

    def _handle_accept(self):
        while True:
            sock, (ip, port) = self.server.accept()
            con = Connection(sock)
            self.connections[sock] = con
            print('New client: from {}:{}'.format(ip, port))

    def _handle_data(self):
        while True:
            # TODO: Might race if not (list)
            socks = list(self.connections.keys())
            ready_to_read, _, _ = select.select(socks, [], [], Consts.TIMEOUT_SELECT_DATA)

            for sock in ready_to_read:
                data = sock.recv(16, socket.MSG_DONTWAIT | socket.MSG_PEEK)
                if len(data) == 0:
                    sock.close()
                    self.connections.pop(sock)
                data = sock.recv(Consts.MAX_MSG_LENGTH)
                self._broadcast(msg=data, origin=sock)

    def _handle_manage(self):
        while True:
            choice = input('enter "exit" to terminate')
            if choice == 'exit':
                return True
