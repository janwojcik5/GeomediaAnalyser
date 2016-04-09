class Article():
    def __init__(self):
        self.tags = []

    def add_tag(self, tag):
        self.tags.append(tag)

    def has_tag(self):
        return len(self.tags) > 0