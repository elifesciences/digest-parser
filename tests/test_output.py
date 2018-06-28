# coding=utf-8

import os
import unittest
from ddt import ddt, data
from digestparser import output
from digestparser.parse import parse_content
from tests import test_data_path, fixture_file


@ddt
class TestOutput(unittest.TestCase):

    def setUp(self):
        pass

    """
    @data(
        {
            'file_name': 'DIGEST 99999.docx',
            'output_dir': 'tmp',
            'expected_docx_file': 'Anonymous 99999.docx'
        },
        )
    def test_build_docx(self, test_data):
        "check building a DOCX from a DOCX file"
        file_name = test_data.get('file_name')
        output_dir = test_data.get('output_dir')
        output_file_name = test_data.get('expected_docx_file')
        expected_fixture = fixture_file(test_data.get('expected_docx_file'))
        # build now
        docx_file = output.build_docx(test_data_path(file_name), output_file_name, output_dir)
        # assert assertions
        self.assertEqual(docx_file, os.path.join(output_dir, output_file_name))
        # parse and compare the content of the built docx and the fixture docx
        output_content = parse_content(os.path.join(output_dir, output_file_name))
        expected_content = parse_content(expected_fixture)
        self.assertEqual(output_content, expected_content)
    """

if __name__ == '__main__':
    unittest.main()
