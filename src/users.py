from user import User


class Users(object):
    DEFAULT_USERS = ['ofek', 'tomer', 'admin']

    def __init__(self, default_initialization=False):
        self.users = {}
        if default_initialization:
            for username in Users.DEFAULT_USERS:
                user = User(username, '1234')
                self.add(user)

    def add(self, user):
        self.users[user.username] = user

    def remove(self, user):
        self.users.pop(user.username)

    def get(self, username):
        return self.users.get(username, None)

    def is_user_exist(self, username):
        user = self.users.get(username)
        if user is None:
            return False
        return True
