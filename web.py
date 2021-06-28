from client import Client
import eel

client = Client()


@eel.expose
def btn_clear():
    return 'cleared'


@eel.expose
def btn_awesome(event):
    return str(event)


@eel.expose
def btn_happy():
    return 'happy'


@eel.expose
def register(username, password):
    print('register')
    status = client.register(username, password)
    if status:
        eel.go_to('/login.html')
    return status


@eel.expose
def login(username, password):
    print('login')
    status = client.login(username, password)
    if status:
        print('goto chat')
        eel.go_to('/chat.html')
    return status


@eel.expose
def get_chats():
    print('get_chats')
    return client.get_chats()


@eel.expose
def get_chat_messages(chat_name):
    print('get_chat_messages')
    return client.get_chat_messages(chat_name)


def main():
    eel.init('web')
    eel.start('login.html', disable_cache=True, size=(400, 675), port=8081)


if __name__ == '__main__':
    main()
