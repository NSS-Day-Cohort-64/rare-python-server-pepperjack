class Post():
    def __init__(self, id, user_id=None, category_id=None, title=None, publication_date=None,
                 image_url=None, content=None, approved=None):
        self.id = id
        self.user_id = user_id
        self.category_id = category_id
        self.title = title
        self.publication_date = publication_date
        self.image_url = image_url
        self.content = content
        self.approved = approved
        self.author = None
        self.category = None
        self.tags = None
