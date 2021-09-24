# coding=utf-8

import os
import unittest
from ddt import ddt, data
from tests import read_fixture, data_path
from digestparser.conf import raw_config, parse_raw_config
from digestparser import build


@ddt
class TestBuild(unittest.TestCase):
    def setUp(self):
        pass

    @data(
        {
            "file_name": "DIGEST 99999.docx",
            "config_section": "elife",
            "image_file": None,
        },
        {
            "file_name": "DIGEST 99999.zip",
            "config_section": "elife",
            "image_file": "IMAGE 99999.jpeg",
        },
    )
    def test_build_digest(self, test_data):
        "check building a digest object from a DOCX file"
        # note: below after 'the' is a unicode non-breaking space character
        expected_author = u"Anonymous"
        expected_title = u"Fishing for errors in the\xa0tests"
        expected_summary = (
            u"Testing a document which mimics the format of a file we’ve used  "
            + "before plus CO<sub>2</sub> and Ca<sup>2+</sup>."
        )
        expected_keywords = ["Face Recognition", "Neuroscience", "Vision"]
        expected_doi = u"https://doi.org/10.7554/eLife.99999"
        expected_text_len = 3
        expected_text_0 = read_fixture("digest_content_99999_text_1.txt").decode(
            "utf-8"
        )
        expected_text_1 = read_fixture("digest_content_99999_text_2.txt").decode(
            "utf-8"
        )
        expected_text_2 = read_fixture("digest_content_99999_text_3.txt").decode(
            "utf-8"
        )
        expected_image_caption = (
            u"<b>It’s not just mammals who can recognise sample data.</b>"
            + u"\xa0Image credit:\xa0Anonymous and Anonymous\xa0(CC BY\xa04.0)"
        )
        # build now
        digest_config = parse_raw_config(raw_config(test_data.get("config_section")))
        digest = build.build_digest(
            data_path(test_data.get("file_name")), "tmp", digest_config
        )
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
            if test_data.get("image_file"):
                expected_image_file = os.path.join("tmp", test_data.get("image_file"))
                self.assertEqual(digest.image.file, expected_image_file)

    def test_build_singleton_blank_content(self):
        "test parsing from blank content for coverage"
        self.assertIsNone(build.build_singleton("title", ""))

    def test_build_keywords_blank_content(self):
        "test parsing keywords from blank content for coverage"
        self.assertIsNone(build.build_keywords(""))

    def test_build_image_blank_content(self):
        "test parsing image content from blank content for coverage"
        self.assertIsNone(build.build_image(""))

    def test_build_image_whitespace(self):
        """test parsing an image credit with whitespace"""
        image_credit = "Anon (CC BY 4.0)\n\n\n"
        expected_image_credit = image_credit.rstrip()
        image_file_name = "digest-41540.jpg"
        content = " <b>IMAGE CREDIT</b> \n%s" % image_credit
        image_object = build.build_image(content, image_file_name)
        self.assertEqual(image_object.caption, expected_image_credit)
        self.assertEqual(image_object.file, image_file_name)

    def test_build_doi_manuscript_number(self):
        "test parsing a doi with manuscript number, prefers manuscript number"
        content = """
<b>MANUSCRIPT NUMBER</b>
11111
<b>FULL ARTICLE DOI</b>
https://doi.org/10.7554/eLife.99999
        """
        digest_config = {"doi_pattern": "https://doi.org/10.7554/eLife.{msid:0>5}"}
        expected_doi = "https://doi.org/10.7554/eLife.11111"
        doi = build.build_doi(content, digest_config)
        self.assertEqual(doi, expected_doi)

    def test_build_doi_no_manuscript_number(self):
        "test parsing a doi if no manuscript number is parsed"
        content = """
<b>FULL ARTICLE DOI</b>
https://doi.org/10.7554/eLife.99999
        """
        digest_config = {}
        expected_doi = "https://doi.org/10.7554/eLife.99999"
        doi = build.build_doi(content, digest_config)
        self.assertEqual(doi, expected_doi)

    def test_build_author_whitespace(self):
        """test parsing an author name with trailing whitespace"""
        author_name = "Author Name"
        content = "<b>AUTHOR</b>\n%s " % author_name
        self.assertEqual(build.build_author(content), author_name)

    def test_build_author_none(self):
        """test for when author is none"""
        content = "<b>AUTHOR INCORRECT HEADING NAME</b>\nAuthor Name"
        self.assertIsNone(build.build_author(content))


if __name__ == "__main__":
    unittest.main()
