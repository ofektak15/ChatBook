import time
from threading import Thread

from message import LoginRequest, RegisterRequest, SendMessageRequest
import socket

from server import PORT


def register(sock):
    request = RegisterRequest()
    username = input('username: ')
    password = input('password: ')

    request.username = username
    request.password = password

    sock.send(request.pack().encode())
    status = sock.recv(1024).decode()
    if status == 'SUCCESS':
        return True
    return False


def login(sock):
    request = LoginRequest()
    username = input('username: ')
    password = input('password: ')

    request.username = username
    request.password = password

    sock.send(request.pack().encode())
    status = sock.recv(1024).decode()
    if status == 'SUCCESS':
        return username
    return None


def send_message(sock, username):
    thread_recv = Thread(target=handle_recv, args=(sock,))
    thread_recv.start()

    while True:
        request = SendMessageRequest()
        recipient = input('recipient: ')
        message_content = input('content: ')

        request.username = username
        request.recipient = recipient
        request.message_content = message_content

        sock.send(request.pack().encode())
        status = sock.recv(1024).decode()
        if status == 'SUCCESS':
            return True
        return False


def handle_recv(sock):
    while True:
        time.sleep(2)
        data = sock.recv(1024).decode()

        if data:
            message = SendMessageRequest()
            message.unpack(data)
            print('Got message "', message.message_content, '" From "', message.username, '"')


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', PORT))
    while True:
        print('[1] Register')
        print('[2] Login')

        choice = input('Enter: ')
        if choice == '1':
            if register(sock):
                print('Register Success :)')
        elif choice == '2':
            username = login(sock)
            if isinstance(username, str):
                print('Login Success :)')
                send_message(sock, username)


if __name__ == '__main__':
    main()
