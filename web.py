import eel


@eel.expose
def btn_clear():
    return 'cleared'


@eel.expose
def btn_awesome(event):
    return str(event)


@eel.expose
def btn_happy():
    return 'happy'


def main():
    eel.init('web')
    eel.start('index.html', disable_cache=True, size=(400, 675))


if __name__ == '__main__':
    main()
