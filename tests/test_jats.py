# coding=utf-8

import unittest
from ddt import ddt, data
from elifetools.utils import date_struct
from tests import read_fixture, data_path, fixture_file
from digestparser.objects import Digest
from digestparser import jats


@ddt
class TestJats(unittest.TestCase):
    def setUp(self):
        pass

    def test_html_to_xml(self):
        "simple test of converting HTML to XML for the digest content"
        html_content = (
            "<b>A <i>simple</i> example</b> to test > 1 & <blink>check</blink>."
        )
        expected_content = (
            "<bold>A <italic>simple</italic> example</bold> to test &gt; 1 "
            + "&amp; &lt;blink&gt;check&lt;/blink&gt;."
        )
        xml_content = jats.html_to_xml(html_content)
        self.assertEqual(xml_content, expected_content)

    def test_xml_to_html(self):
        "test converting XML to HTML"
        xml_content = (
            "<bold>A <italic>simple</italic> example</bold> to test &gt; 1 &amp; "
            + "<blink>check</blink>."
        )
        expected_content = (
            "<b>A <i>simple</i> example</b> to test &gt; 1 &amp; &lt;blink&gt;"
            + "check&lt;/blink&gt;."
        )
        html_content = jats.xml_to_html(xml_content)
        self.assertEqual(html_content, expected_content)

    def test_digest_jats(self):
        "simple test to convert digest text to JATS XML content"
        digest = Digest()
        digest.text = [
            "First <b>paragraph</b>.",
            "Second <i>paragraph</i>.",
            "",
            " ",
            None,
        ]
        expected_content = (
            "<p>First <bold>paragraph</bold>.</p><p>Second "
            + "<italic>paragraph</italic>.</p>"
        )
        jats_content = jats.digest_jats(digest)
        self.assertEqual(jats_content, expected_content)

    def test_build_jats(self):
        "check building JATS XML content from a DOCX file"
        docx_file = "DIGEST 99999.docx"
        expected_content = read_fixture("jats_content_99999.txt").decode("utf-8")
        jats_content = jats.build_jats(data_path(docx_file))
        self.assertEqual(jats_content, expected_content)

    @data(
        {"string": None, "expected": None},
        {
            "string": "<p>One</p><p><italic>Two</italic></p>",
            "expected": ["One", "<italic>Two</italic>"],
        },
    )
    def test_split_paragraphs(self, test_data):
        "check building JATS XML content from a DOCX file"
        content = jats.split_paragraphs(test_data.get("string"))
        self.assertEqual(content, test_data.get("expected"))

    def test_parse_jats_digest(self):
        "extract text content from a JATS file abstract digest"
        soup = jats.parse_jats_file(fixture_file("elife-99999-v0.xml"))
        content = jats.parse_jats_digest(soup)
        expected_content = read_fixture("elife_99999_v0_digest.py")
        self.assertEqual(content, expected_content)

    def test_parse_jats_pub_date(self):
        "extract pub date from a JATS file"
        soup = jats.parse_jats_file(fixture_file("elife-99999-v0.xml"))
        pub_date = jats.parse_jats_pub_date(soup)
        self.assertEqual(pub_date, date_struct(2018, 8, 1))


if __name__ == "__main__":
    unittest.main()
