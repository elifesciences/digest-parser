"""
Digest object definitions
"""

class Digest(object):
    "Digest object"

    def __new__(cls):
        new_instance = object.__new__(cls)
        new_instance.init()
        return new_instance

    def init(self):
        self.title = None
        self.summary = None
        self.keywords = []
        self.doi = None
        self.text = []
        self.image = None


class Image(object):
    "Image object"

    def __new__(cls):
        new_instance = object.__new__(cls)
        new_instance.init()
        return new_instance

    def init(self):
        self.caption = None
        self.credit = None
        self.license = None
        self.file = None