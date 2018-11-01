# coding=utf-8

import unittest
from ddt import ddt, data, unpack
from tests import data_path
from digestparser.zip import profile_zip


@ddt
class TestZip(unittest.TestCase):

    def setUp(self):
        pass

    @data(
        ('DIGEST 99999.zip', 'DIGEST 99999.docx', 'IMAGE 99999.jpeg'),
        ('DIGEST 99999_with_subfolder.zip', 'DIGEST 99999.docx', 'IMAGE 99999.jpeg'),
    )
    @unpack
    def test_profile_zip(self, zip_file, expected_docx, expected_image):
        "test parsing of zip file to find the docx and image file names"
        docx, image = profile_zip(data_path(zip_file))
        self.assertEqual(docx, expected_docx,
                         'file_name {file_name}, expected {expected}, got {output}'.format(
                             file_name=zip_file, expected=expected_docx, output=docx))
        self.assertEqual(image, expected_image,
                         'file_name {file_name}, expected {expected}, got {output}"'.format(
                             file_name=zip_file, expected=expected_image, output=image))


if __name__ == '__main__':
    unittest.main()
