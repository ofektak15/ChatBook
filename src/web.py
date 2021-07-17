import random
from src.client import Client
import eel

client = Client()  # creating a client


@eel.expose
def register(username, password):
    print('register')
    status = client.register(username, password)
    # if the user succeed in the registration - the screen changes to the page 'login'
    if status:
        eel.go_to('/login.html')
    return status


@eel.expose
def login(username, password):
    print('login - web')
    status = client.login(username, password)
    # if the user succeed in the login - the screen changes to the page 'chat'
    if status:
        print('goto chat')
        eel.go_to('/chat.html')
    return status


@eel.expose
def get_username():
    print("get username - web")
    username = client.get_username()
    return username


@eel.expose
def get_chats():
    print('get_chats')
    return client.get_chats()


@eel.expose
def get_chat_messages(chat_name):
    print('get_chat_messages')
    print(chat_name)
    return client.get_chat_messages(chat_name)


@eel.expose
def send_message(username, chat_name, content, chat_type):
    print('send_message')
    return client.send_message(username, chat_name, content, chat_type)


@eel.expose
def create_private_chat(recipient):
    print('create private chat')
    return client.create_private_chat(recipient)


@eel.expose
def create_group_chat(recipients, group_name):
    print('create group chat')
    return client.create_group_chat(recipients, group_name)


@eel.expose
def log_out(username):
    print("logging out")
    return client.log_out(username)


@eel.expose
def get_is_connected(username):
    print('get_is_connected')
    return client.get_is_connected(username)


@eel.expose
def get_is_update():
    print('get_is_update')
    return client.get_is_update()


def main():
    eel.init('web')
    rnd = random.randint(0, 3000)
    print('using port: {}'.format(8080 + rnd))
    eel.start('login.html', disable_cache=True, size=(400, 675), port=8080 + rnd)


if __name__ == '__main__':
    main()
