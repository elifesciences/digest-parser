# coding=utf-8

import unittest
from digestparser import jats
from tests import test_data_path
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
        expected_content = u'<p>Being able to recognize sample data is crucial for social interactions in humans. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p><p>Some other mammals also identify sample data. For example, female medaka fish (<italic>Oryzias latipes</italic>) prefer sample data they have seen before to ‘strangers’. However, until now, it was not known if they can recognize individual faces, nor how they distinguish a specific male from many others.</p><p>Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?</p>'
        jats_content = jats.build_jats(test_data_path(docx_file))
        self.assertEqual(jats_content, expected_content)


if __name__ == '__main__':
    unittest.main()
