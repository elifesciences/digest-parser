import unittest
import time
import os
from digestparser import parse


def read_file(file_name_plus_path):
    with open(file_name_plus_path, 'rb') as open_file:
        return open_file.read()

def fixture_path(file_name):
    return os.path.join('tests', 'fixtures', file_name)

def read_fixture(file_name):
    return read_file(fixture_path(file_name))

def test_data_path(file_name):
    return os.path.join('tests', 'test_data', file_name)


class TestGenerate(unittest.TestCase):

    def setUp(self):
        pass

    def test_parse_content(self):
        "test parsing all the content"
        expected = read_fixture('digest_99999.txt').decode('utf-8')
        content = parse.parse_content(test_data_path('DIGEST 99999.docx'))
        self.assertEqual(content, expected)


if __name__ == '__main__':
    unittest.main()