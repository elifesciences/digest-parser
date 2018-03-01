import unittest
from digestparser import objects


class TestObjects(unittest.TestCase):

    def setUp(self):
        pass


    def test_digest(self):
        "check instantiating a Digest object"
        digest = objects.Digest()
        self.assertIsNotNone(digest, "digest object is None")
        self.assertIsNone(digest.title, "new digest title is not None")
        self.assertIsNone(digest.summary, "new digest summary is not None")
        self.assertIsNone(digest.doi, "new digest doi is not None")
        self.assertIsNone(digest.image, "new digest image is not None")
        self.assertEqual(digest.keywords, [], "new digest keywords is not empty")
        self.assertEqual(digest.text, [], "new digest text is not empty")


    def test_image(self):
        "check instantiating an Image object"
        image =  objects.Image()
        self.assertIsNotNone(image, "image object is None")
        self.assertIsNone(image.caption, "new image caption is not None")
        self.assertIsNone(image.credit, "new image credit is not None")
        self.assertIsNone(image.license, "new image license is not None")
        self.assertIsNone(image.file, "new image file is not None")


if __name__ == '__main__':
    unittest.main()
