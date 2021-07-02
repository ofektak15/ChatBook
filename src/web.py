import random

from src.client import Client
import eel

client = Client()


@eel.expose
def register(username, password):
    print('register')
    status = client.register(username, password)
    if status:
        eel.go_to('/login.html')
    return status


@eel.expose
def login(username, password):
    print('login - web')
    status = client.login(username, password)
    if status:
        print('goto chat')
        eel.go_to('/chat.html')
    return status


@eel.expose
def get_username():
    username = client.get_username()
    return username


@eel.expose
def get_chats():
    print('get_chats')
    return client.get_chats()


@eel.expose
def get_chat_messages(chat_name):
    print('get_chat_messages')
    return client.get_chat_messages(chat_name)


@eel.expose
def send_message(username, chatname, content, chat_type):
    print('send_message')
    return client.send_message(username, chatname, content, chat_type)


def main():
    eel.init('web')
    rnd = random.randint(0, 1000)
    print('using port: {}'.format(8080 + rnd))
    eel.start('login.html', disable_cache=True, size=(400, 675), port=8080 + rnd)


if __name__ == '__main__':
    main()
