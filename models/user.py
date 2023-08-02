class User:
    """
    new User class
    """
    def __init__(self, id, username, first_name, last_name, email, bio, profile_image_url):
        self.id = id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.bio = bio
        self.profile_image_url = profile_image_url if profile_image_url is not None else "null"
