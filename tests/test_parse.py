import unittest
import time
from digestparser import parse

class TestGenerate(unittest.TestCase):

    def setUp(self):
        pass

    def test_dummy(self):
        self.assertEqual(parse.dummy(), None)


if __name__ == '__main__':
    unittest.main()