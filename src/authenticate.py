class Authenticate(object):
    def __init__(self, users):
        self.users = users

    def authenticate(self, username):
        if self.users.is_user_exist(username):
            if not self.is_user_logged_in(username):
                user = self.users.get(username)
                return user
            else:
                # TODO: handle more error codes
                # user is already logged in
                return None
        else:
            # TODO: handle more error codes
            # user does not exist
            return None

    def is_user_logged_in(self, username):
        user = self.users.get(username)
        if user is None:
            return None
        return user.is_logged_in
