# coding=utf-8

import unittest
import os
from ddt import ddt, data, unpack
from tests import data_path
from digestparser.zip import profile_zip, unzip_zip, zip_output_name


@ddt
class TestZip(unittest.TestCase):

    def setUp(self):
        pass

    @data(
        ('DIGEST 99999.zip', 'DIGEST 99999.docx', 'IMAGE 99999.jpeg'),
        ('DIGEST 99999_with_subfolder.zip', 'DIGEST 99999.docx', 'IMAGE 99999.jpeg'),
        ('DIGEST 35774.zip', 'Bayés_35774.docx', 'bayes.jpg'),
    )
    @unpack
    def test_profile_zip(self, zip_file, expected_docx, expected_image):
        "test parsing of zip file to find the docx and image file names"
        docx, image = profile_zip(data_path(zip_file))
        docx_file_name = zip_output_name(docx.filename, '')
        image_file_name = zip_output_name(image.filename, '')
        self.assertEqual(docx_file_name, expected_docx,
                         'file_name {file_name}, expected {expected}, got {output}'.format(
                             file_name=zip_file, expected=expected_docx, output=docx))
        self.assertEqual(image_file_name, expected_image,
                         'file_name {file_name}, expected {expected}, got {output}"'.format(
                             file_name=zip_file, expected=expected_image, output=image))

    def test_unzip_zip(self):
        "test parsing of zip file to find the docx and image file names"
        zip_file = 'DIGEST 35774.zip'
        temp_dir = 'tmp'
        docx, image = unzip_zip(data_path(zip_file), 'tmp')
        expected_docx = os.path.join(temp_dir, 'Bayés_35774.docx')
        expected_image = os.path.join(temp_dir, 'bayes.jpg')
        self.assertEqual(docx, expected_docx,
                         'expected {expected}, got {output}'.format(
                             expected=expected_docx, output=docx))
        self.assertEqual(image, expected_image,
                         'expected {expected}, got {output}'.format(
                             expected=expected_image, output=docx))


if __name__ == '__main__':
    unittest.main()
