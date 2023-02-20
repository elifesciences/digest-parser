# coding=utf-8

import unittest
import os
from ddt import ddt, data, unpack
from digestparser.utils import sanitise, formatter_string, msid_from_doi


@ddt
class TestUtils(unittest.TestCase):
    def setUp(self):
        pass

    @data(
        (None, None),
        ("", ""),
        ("file.docx", "file.docx"),
        ("../../file.docx", "file.docx"),
        ("/file.docx", "file.docx"),
        ("\\file.docx", "file.docx"),
        ("Bayés.docx", "Bayés.docx"),
    )
    @unpack
    def test_sanitise(self, file_name, expected):
        "test sanitise of file names"
        output = sanitise(file_name)
        self.assertEqual(
            output,
            expected,
            "file_name {file_name}, expected {expected}, got {output}".format(
                file_name=file_name, expected=expected, output=output
            ),
        )

    @data(
        ("folder", "Bayés_35774.docx"),
    )
    @unpack
    def test_sanitise_join(self, folder_name, file_name):
        "test os.path.join of sanitised file names"
        expected = "".join([folder_name, os.sep, file_name])
        sanitised_file_name = sanitise(file_name)
        output = os.path.join(folder_name, sanitised_file_name)
        self.assertEqual(
            output,
            expected,
            (
                "folder_name {folder_name}, file_name {file_name}, "
                + "expected {expected}, got {output}"
            ).format(
                folder_name=folder_name,
                file_name=file_name,
                expected=expected,
                output=output,
            ),
        )

    @data(
        (None, None, ""),
        ({"test": "ignored"}, "not_an_attribute", ""),
        ({"test": "exists"}, "test", "exists"),
    )
    @unpack
    def test_formatter_string(self, content, attribute, expected):
        "test returing blank string for some expected inputs"
        output = formatter_string(content, attribute)
        fail_msg = "content {content}, attribute {attribute}, expected {expected}, got {output}"
        self.assertEqual(
            output,
            expected,
            fail_msg.format(
                content=content, attribute=attribute, expected=expected, output=output
            ),
        )

    def test_msid_from_doi(self):
        cases = [
            ('10.7554/eLife.09560', 9560),
            # component
            ('10.7554/eLife.09560.sa0', 9560),
            # versioned
            ('10.7554/eLife.09560.1', 9560),
            ('10.7554/eLife.09560.1.sa0', 9560),
            # testing msid
            ('10.7554/eLife.97832421234567890', 97832421234567890),
            # case insensitive
            ('10.7554/ELIFE.09560', 9560),
            # unlikely cases
            ('10.7554/eLife.0', 0),
            ('10.7554/eLife.0.1', 0),
            ('10.7554/eLife.0.1.2.3.4', 0),

            # no match cases
            (None, None),
            ('', None),
            ([], None),
            ({}, None),
            ('not_a_doi', None),
        ]
        for given, expected in cases:
            self.assertEqual(msid_from_doi(given), expected, "failed case %r" % given )


if __name__ == "__main__":
    unittest.main()
