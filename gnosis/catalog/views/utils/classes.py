# comments specific to a user
class UserComment:
    def __init__(self, comment, is_hidden):
        self.id = comment.id
        self.author = comment.author
        self.text = comment.text
        self.publication_date = comment.publication_date
        self.created_by = comment.created_by
        self.created = comment.created
        self.is_hidden = is_hidden

    def is_hidden(self):
        return self.is_hidden
