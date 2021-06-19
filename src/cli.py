from client import Client
from server import Server

IP = '127.0.0.1'
PORT = 1342


def start_server():
    server = Server(IP, PORT)
    server.start()


def start_client():
    client = Client(IP, PORT)
    client.start()


def main():
    while True:
        print('[1] Server')
        print('[2] Client')
        choice = input('Choice:')
        if choice == '1':
            start_server()
        elif choice == '2':
            start_client()


if __name__ == '__main__':
    main()
