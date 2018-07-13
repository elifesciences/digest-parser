# coding=utf-8

import unittest
from ddt import ddt, data
from digestparser import json_output
from tests import read_fixture, test_data_path, fixture_file


@ddt
class TestJsonOutput(unittest.TestCase):

    def setUp(self):
        pass

    @data(
        {
            'file_name': 'DIGEST 99999.docx',
            'jats_file': 'elife-99999-v0.xml',
            'expected_json_file': 'json_content_99999.py'
        },
        )
    def test_build_json(self, test_data):
        "check building a JSON from a DOCX file"
        file_name = test_data_path(test_data.get('file_name'))
        jats_file = fixture_file(test_data.get('jats_file'))
        expected_json = read_fixture(test_data.get('expected_json_file'))
        # build now
        json_content = json_output.build_json(file_name, jats_file)
        # assert assertions
        self.assertEqual(json_content, expected_json)


if __name__ == '__main__':
    unittest.main()
