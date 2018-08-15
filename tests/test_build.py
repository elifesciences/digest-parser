# coding=utf-8

import os
import unittest
from ddt import ddt, data
from tests import read_fixture, test_data_path
from digestparser import build


@ddt
class TestBuild(unittest.TestCase):

    def setUp(self):
        pass

    @data(
        {
            'file_name': 'DIGEST 99999.docx',
            'config_section': 'elife',
            'image_file': None
        },
        {
            'file_name': 'DIGEST 99999.zip',
            'config_section': 'elife',
            'image_file': 'IMAGE 99999.jpeg'
        }
        )
    def test_build_digest(self, test_data):
        "check building a digest object from a DOCX file"
        # note: below after 'the' is a unicode non-breaking space character
        expected_author = u'Anonymous'
        expected_title = u'Fishing for errors in the\xa0tests'
        expected_summary = (u'Testing a document which mimics the format of a file we’ve used  ' +
                            'before plus CO<sub>2</sub> and Ca<sup>2+</sup>.')
        expected_keywords = ['Face Recognition', 'Neuroscience', 'Vision']
        expected_doi = u'https://doi.org/10.7554/eLife.99999'
        expected_text_len = 3
        expected_text_0 = read_fixture('digest_content_99999_text_1.txt').decode('utf-8')
        expected_text_1 = read_fixture('digest_content_99999_text_2.txt').decode('utf-8')
        expected_text_2 = read_fixture('digest_content_99999_text_3.txt').decode('utf-8')
        expected_image_caption = u'<b>It’s not just mammals who can recognise sample data.</b>'
        expected_image_credit = u'Anonymous and Anonymous'
        expected_image_license = u'CC BY 4.0'
        # build now
        digest = build.build_digest(test_data_path(test_data.get('file_name')),
                                    'tmp',
                                    test_data.get('config_section'))
        # assert assertions
        self.assertIsNotNone(digest)
        self.assertEqual(digest.author, expected_author)
        self.assertEqual(digest.title, expected_title)
        self.assertEqual(digest.summary, expected_summary)
        self.assertEqual(digest.keywords, expected_keywords)
        self.assertEqual(digest.doi, expected_doi)
        self.assertEqual(len(digest.text), expected_text_len)
        self.assertEqual(digest.text[0], expected_text_0)
        self.assertEqual(digest.text[1], expected_text_1)
        self.assertEqual(digest.text[2], expected_text_2)
        if digest.image:
            self.assertEqual(digest.image.caption, expected_image_caption)
            self.assertEqual(digest.image.credit, expected_image_credit)
            self.assertEqual(digest.image.license, expected_image_license)
            if test_data.get('image_file'):
                expected_image_file = os.path.join('tmp', test_data.get('image_file'))
                self.assertEqual(digest.image.file, expected_image_file)

    def test_build_singleton_blank_content(self):
        "test parsing from blank content for coverage"
        self.assertIsNone(build.build_singleton('title', ''))

    def test_build_keywords_blank_conten(self):
        "test parsing keywords from blank content for coverage"
        self.assertIsNone(build.build_keywords(''))

    def test_build_image_blank_conten(self):
        "test parsing image content from blank content for coverage"
        self.assertIsNone(build.build_image(''))


if __name__ == '__main__':
    unittest.main()
