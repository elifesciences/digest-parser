# coding=utf-8

import unittest
from digestparser import build, html
from tests import read_fixture, test_data_path


class TestHtml(unittest.TestCase):

    def setUp(self):
        pass

    def test_string_to_html(self):
        "test of converting content string to HTML"
        string_content = ("<b>A <i>simple</i> example</b> <sup>to <sub>test</sub></sup> > 1 & " +
                          "<blink>check</blink>.")
        expected_content = ("<b>A <i>simple</i> example</b> <sup>to <sub>test</sub></sup> &gt; " +
                            "1 &amp; &lt;blink&gt;check&lt;/blink&gt;.")
        html_content = html.string_to_html(string_content)
        self.assertEqual(html_content, expected_content)

    def test_build_to_html(self):
        "test building from a DOCX file and converting to HTML"
        docx_file = 'DIGEST 99999.docx'
        expected_title = u'Fishing for errors in the tests'
        expected_summary = read_fixture('html_content_99999_summary.txt').decode('utf-8')
        expected_text_1 = read_fixture('html_content_99999_text_1.txt').decode('utf-8')
        expected_text_2 = read_fixture('html_content_99999_text_2.txt').decode('utf-8')
        expected_text_3 = read_fixture('html_content_99999_text_3.txt').decode('utf-8')
        # build the digest object
        digest = build.build_digest(test_data_path(docx_file))
        # test assertions
        self.assertEqual(html.string_to_html(digest.title), expected_title)
        self.assertEqual(html.string_to_html(digest.summary), expected_summary)
        self.assertEqual(html.string_to_html(digest.text[0]), expected_text_1)
        self.assertEqual(html.string_to_html(digest.text[1]), expected_text_2)
        self.assertEqual(html.string_to_html(digest.text[2]), expected_text_3)


if __name__ == '__main__':
    unittest.main()
