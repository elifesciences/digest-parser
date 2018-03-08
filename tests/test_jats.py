# coding=utf-8

import unittest
from digestparser import jats
from tests import read_fixture, test_data_path
from digestparser.objects import Digest

class TestJats(unittest.TestCase):

    def setUp(self):
        pass


    def test_html_to_xml(self):
        "simple test of converting HTML to XML for the digest content"
        html_content = "<b>A <i>simple</i> example</b> to test > 1 & <blink>check</blink>."
        expected_content = "<bold>A <italic>simple</italic> example</bold> to test &gt; 1 &amp; &lt;blink&gt;check&lt;/blink&gt;."
        xml_content = jats.html_to_xml(html_content)
        self.assertEqual(xml_content, expected_content)


    def test_digest_jats(self):
        "simple test to convert digest text to JATS XML content"
        digest = Digest()
        digest.text = [
            "First <b>paragraph</b>.",
            "Second <i>paragraph</i>.",
        ]
        expected_content = "<p>First <bold>paragraph</bold>.</p><p>Second <italic>paragraph</italic>.</p>"
        jats_content = jats.digest_jats(digest)
        self.assertEqual(jats_content, expected_content)


    def test_build_jats(self):
        "check building JATS XML content from a DOCX file"
        docx_file = 'DIGEST 99999.docx'
        expected_content = read_fixture('jats_content_99999.txt').decode('utf-8')
        jats_content = jats.build_jats(test_data_path(docx_file))
        self.assertEqual(jats_content, expected_content)


if __name__ == '__main__':
    unittest.main()
