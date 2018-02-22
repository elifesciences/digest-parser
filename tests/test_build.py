import unittest
from digestparser import build
from tests import test_data_path


class TestBuild(unittest.TestCase):

    def setUp(self):
        pass


    def test_build_digest(self):
        "check building a digest object from a DOCX file"
        digest = build.build_digest(test_data_path('DIGEST 99999.docx'))
        self.assertIsNotNone(digest)


if __name__ == '__main__':
    unittest.main()
