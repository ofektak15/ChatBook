class User(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password

        self.is_logged_in = False
