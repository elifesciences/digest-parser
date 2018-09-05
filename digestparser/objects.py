"""
Digest object definitions
"""


class Digest(object):
    "Digest object"

    def __new__(cls):
        new_instance = object.__new__(cls)
        new_instance.__init__()
        return new_instance

    def __init__(self):
        self.author = None
        self.title = None
        self.summary = None
        self.keywords = []
        self.manuscript_number = None
        self.doi = None
        self.text = []
        self.image = None
        self.published = None
        self.subjects = []


class Image(object):
    "Image object"

    def __new__(cls):
        new_instance = object.__new__(cls)
        new_instance.__init__()
        return new_instance

    def __init__(self):
        self.caption = None
        self.file = None
