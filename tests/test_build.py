# coding=utf-8

import os
import unittest
from digestparser import build
from tests import test_data_path
from ddt import ddt, data

@ddt
class TestBuild(unittest.TestCase):

    def setUp(self):
        pass

    @data(
        {
            'file_name': 'DIGEST 99999.docx',
            'image_file': None
        },
        {
            'file_name': 'DIGEST 99999.zip',
            'image_file': 'IMAGE 99999.jpeg'
        }
        )
    def test_build_digest(self, test_data):
        "check building a digest object from a DOCX file"
        file_name = test_data.get('file_name')
        # note: below after 'the' is a unicode non-breaking space character
        expected_title = u'Fishing for errors in the\xa0tests'
        expected_summary = u'Testing a document which mimics the format of a file we’ve used  before plus CO<sub>2</sub> and Ca<sup>2+</sup>.'
        expected_keywords = ['Face Recognition', 'Neuroscience', 'Vision']
        expected_doi = u'https://doi.org/10.7554/eLife.99999'
        expected_text_len = 3
        expected_text_0 = u'Being able to recognize sample data is crucial for social interactions in humans. This is also added, CO<sub>2</sub> or Ca<sup>2+</sup>, & 1 < 2. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
        expected_text_1 = u'Some other mammals also identify sample data. For example, female medaka fish (<i>Oryzias latipes</i>) prefer sample data they have seen before to ‘strangers’. However, until now, it was not known if they can recognize individual faces, nor how they distinguish a specific male from many others.'
        expected_text_2 = u'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?'
        expected_image_caption = u'<b>It’s not just mammals who can recognise sample data.</b>'
        expected_image_credit = u'Anonymous and Anonymous'
        expected_image_license = u'CC BY 4.0'
        # build now
        digest = build.build_digest(test_data_path(file_name))
        # assert assertions
        self.assertIsNotNone(digest)
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
