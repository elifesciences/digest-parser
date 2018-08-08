# coding=utf-8

import os
import unittest
from ddt import ddt, data
from digestparser import output
from digestparser.objects import Digest
from digestparser.parse import parse_content
from digestparser.build import build_digest
from digestparser.conf import raw_config, parse_raw_config
from tests import test_data_path, fixture_file


@ddt
class TestOutput(unittest.TestCase):

    def setUp(self):
        pass

    @data(
        {
            'file_name': 'DIGEST 99999.docx',
            'output_dir': 'tmp',
            'expected_docx_file': 'Anonymous_99999.docx'
        },
        )
    def test_build_docx(self, test_data):
        "check building a DOCX from a DOCX file"
        file_name = test_data.get('file_name')
        output_dir = test_data.get('output_dir')
        digest = build_digest(test_data_path(file_name))
        output_file_name = output.docx_file_name(digest)
        expected_fixture = fixture_file(test_data.get('expected_docx_file'))
        # build now
        docx_file = output.build_docx(test_data_path(file_name), output_file_name, output_dir)
        # assert assertions
        self.assertEqual(docx_file, os.path.join(output_dir, output_file_name))
        # parse and compare the content of the built docx and the fixture docx
        output_content = parse_content(os.path.join(output_dir, output_file_name))
        expected_content = parse_content(expected_fixture)
        self.assertEqual(output_content, expected_content)

    def test_digest_docx(self):
        "test digest_docx directly for coverage of setting bold tags"
        output_dir = 'tmp'
        output_file_name = 'bold_tag_test.docx'
        text = ['<b>Test</b>']
        expected_content = "DIGEST\n<b>Test</b>\n"
        digest = Digest()
        digest.text = text
        docx_file = output.digest_docx(digest, output_file_name, output_dir)
        output_content = parse_content(docx_file)
        self.assertEqual(output_content, expected_content)

    @data(
        {
            'scenario': 'all digest data using a default config',
            'author': 'Anonymous',
            'doi': '10.7554/eLife.99999',
            'use_config': True,
            'config_section': None,
            'expected_file_name': 'Anonymous_99999.docx'
        },
        {
            'scenario': 'all digest data and not using a config',
            'author': u'Anonymous',
            'doi': '10.7554/eLife.99999',
            'use_config': False,
            'expected_file_name': u'Anonymous_99999.docx'
        },
        {
            'scenario': 'missing digest data and not using a config',
            'author': None,
            'doi': None,
            'use_config': False,
            'expected_file_name': 'None_0None.docx'
        },
        {
            'scenario': 'unicode author name using a default config',
            'author': u'Nö',
            'doi': '10.7554/eLife.99999',
            'use_config': True,
            'config_section': None,
            'expected_file_name': u'Nö_99999.docx'
        },
        {
            'scenario': 'unicode author name and not using a config',
            'author': u'Nö',
            'doi': '10.7554/eLife.99999',
            'use_config': False,
            'expected_file_name': u'Nö_99999.docx'
        },
        {
            'scenario': 'ugly ugly author name and not using a config',
            'author': u'‘“Nö(%)”/\\:"<>|*’',
            'doi': '10.7554/eLife.99999',
            'use_config': False,
            'expected_file_name': u"'Nö(%)'_99999.docx"
        },
    )
    def test_docx_file_name(self, test_data):
        "docx output file name tests for various input"
        # build the Digest object
        digest = Digest()
        digest.author = test_data.get('author')
        digest.doi = test_data.get('doi')
        # set the config, if using in the test
        digest_config = None
        if test_data.get('use_config'):
            digest_config = parse_raw_config(raw_config(test_data.get('config_section')))
        # generate the file_name
        file_name = output.docx_file_name(digest, digest_config)
        # test assertion
        self.assertEqual(
            file_name, test_data.get('expected_file_name'),
            u"failed in scenario '{scenario}', got file_name {file_name}".format(
                scenario=test_data.get('scenario'),
                file_name=file_name
                ))
        # test for creating the file on disk
        output_file_name = output.digest_docx(digest, file_name, 'tmp')
        self.assertEqual(
            os.path.join('tmp', test_data.get('expected_file_name')),
            output_file_name,
            u"failed creating file in scenario '{scenario}', got file_name {file_name}".format(
                scenario=test_data.get('scenario'),
                file_name=output_file_name
                ))


if __name__ == '__main__':
    unittest.main()
