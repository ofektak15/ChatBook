class Message:
    command_id = ""
    username = ""

    def __init__(self, command_id, username):
        self.command_id = command_id
        self.username = username

    def pack(self):
        return
    


