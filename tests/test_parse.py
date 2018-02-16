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


    def test_html_open_close_tag_failure(self):
        "test getting an open and close tag for a style that does not exist"
        style = "not_a_style"
        expected = None, None
        self.assertEqual(parse.html_open_close_tag(style), expected)


    def test_open_close_style_failure(self):
        "test wrapping content in close and open tags for a style that does not exist"
        run = None
        prev_run = None
        output = ''
        style = "not_a_style"
        expected = output
        self.assertEqual(parse.open_close_style(run, prev_run, output, style), expected)


if __name__ == '__main__':
    unittest.main()