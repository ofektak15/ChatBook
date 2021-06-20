import select
import socket
from threading import Thread

from connection import Connection
from connections import Connections
from const import Consts


class Server(object):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.server.bind((self.ip, self.port))
        self.server.listen(Consts.MAX_SERVER_LISTEN)

        self.thread_accept = None
        self.thread_data = None
        self.thread_manage = None

        self.connections = Connections()
        # [1,2,3,4,5,6,7,8,9,10] (O(n))
        # {'1': 1, ... , '9': 9 } (O(1))

    def start(self):
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
        connections = list(self.connections.get_connections())
        for connection in connections:
            if connection == origin:
                continue
            # TODO: Might throw exception if the socket was closed already *race*
            connection.send(msg)

    def _handle_accept(self):
        while True:
            sock, (ip, port) = self.server.accept()
            connection = Connection(sock)
            self.connections.add(connection)
            print('New client: from {}:{}'.format(ip, port))

    def _handle_data(self):
        while True:
            # TODO: Might race if not (list)
            socks = list(self.connections.get_socks())
            ready_to_read, _, _ = select.select(socks, [], [], Consts.TIMEOUT_SELECT_DATA)

            for sock in ready_to_read:
                connection = self.connections.get(sock)
                self._handle_connection(connection)

    def _handle_manage(self):
        while True:
            choice = input('enter "exit" to terminate')
            if choice == 'exit':
                return True

    def _handle_connection(self, connection):
        if connection.is_closed():
            connection.close()
            self.connections.remove(connection)
        data = connection.recv(Consts.MAX_MSG_LENGTH)
        self._broadcast(msg=data, origin=connection)
