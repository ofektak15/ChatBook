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
    return client.register(username, password)


@eel.expose
def login(username, password):
    print('login')
    return client.login(username, password)


def main():
    eel.init('web')
    eel.start('login.html', disable_cache=True, size=(400, 675), port=8081)


if __name__ == '__main__':
    main()
