# coding=utf-8

import unittest
from ddt import ddt, data, unpack
from digestparser.utils import sanitise

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


if __name__ == '__main__':
    unittest.main()
