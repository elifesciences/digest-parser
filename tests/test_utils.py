# coding=utf-8

import unittest
from ddt import ddt, data, unpack
from digestparser.utils import sanitise, formatter_string


@ddt
class TestUtils(unittest.TestCase):

    def setUp(self):
        pass

    @data(
        (None, None),
        ('', ''),
        ('file.docx', 'file.docx'),
        ('../../file.docx', 'file.docx'),
        ('/file.docx', 'file.docx'),
        ('\\file.docx', 'file.docx'),
    )
    @unpack
    def test_sanitise(self, file_name, expected):
        "test sanitise of file names"
        output = sanitise(file_name)
        self.assertEqual(output, expected,
                         'file_name {file_name}, expected {expected}, got {output}'.format(
                             file_name=file_name, expected=expected, output=output))

    @data(
        (None, None, ''),
        ({'test': 'ignored'}, 'not_an_attribute', ''),
        ({'test': 'exists'}, 'test', 'exists'),
    )
    @unpack
    def test_formatter_string(self, content, attribute, expected):
        "test returing blank string for some expected inputs"
        output = formatter_string(content, attribute)
        fail_msg = 'content {content}, attribute {attribute}, expected {expected}, got {output}'
        self.assertEqual(output, expected, fail_msg.format(
            content=content, attribute=attribute, expected=expected, output=output))


if __name__ == '__main__':
    unittest.main()
