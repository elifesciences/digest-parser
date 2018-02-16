import unittest
import os
from ddt import ddt, data, unpack
from digestparser import parse


def read_file(file_name_plus_path):
    "read file content"
    with open(file_name_plus_path, 'rb') as open_file:
        return open_file.read()

def fixture_path(file_name):
    "path for a file in the fixtures directory"
    return os.path.join('tests', 'fixtures', file_name)

def read_fixture(file_name):
    "read a file from the fixtures directory"
    return read_file(fixture_path(file_name))

def test_data_path(file_name):
    "path for a file in the test_data directory"
    return os.path.join('tests', 'test_data', file_name)


@ddt
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
        self.assertEqual(parse.run_open_close_style(run, prev_run, output, style), expected)

    @unpack
    @data(
        (None, None, None, '', 'italic', ''),
        # previous run is italic, current run is not
        (True, None, None, '', 'italic', '</i>'),
        # previous run is italic, current run is also italic
        (True, True, None, '', 'italic', ''),
        # previous run is not italic, current run is italic
        (None, True, None, '', 'italic', '<i>'),
        # previous run is not italic, current run is italic, output ends in a new line
        (None, True, None, 'test\n', 'italic', 'test\n<i>'),
        # previous run italic and contains a break, current run italic, output ends in a new line
        (True, True, True, 'test\n', 'italic', 'test</i>\n<i>'),
        )
    def test_open_close_style(self, one_has_attr, two_has_attr, one_contains_break, output, attr,
                              expected):
        "test the open close tag logic with basic attributes"
        self.assertEqual(parse.open_close_style(
            one_has_attr, two_has_attr, one_contains_break, output, attr), expected)


if __name__ == '__main__':
    unittest.main()
