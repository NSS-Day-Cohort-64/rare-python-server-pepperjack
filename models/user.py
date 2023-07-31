class User:
    def __init__(self, username, first_name, last_name, email, password, bio=None):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.bio = bio
