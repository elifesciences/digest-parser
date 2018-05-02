# coding=utf-8

import unittest
from digestparser import medium_post
from tests import read_fixture, test_data_path

class TestMedium(unittest.TestCase):

    def setUp(self):
        pass


    def test_build_medium_content(self):
        "test building from a DOCX file and converting to Medium content"
        config_section = 'elife'
        docx_file = 'DIGEST 99999.docx'
        expected_medium_content = read_fixture('medium_content_99999.py')
        # build the digest object
        medium_content = medium_post.build_medium_content(test_data_path(docx_file), config_section)
        # test assertions
        self.assertEqual(medium_content, expected_medium_content)


if __name__ == '__main__':
    unittest.main()
