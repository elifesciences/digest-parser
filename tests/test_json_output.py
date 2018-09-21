# coding=utf-8

import unittest
from collections import OrderedDict
from mock import patch
from ddt import ddt, data
from digestparser import json_output
from digestparser.objects import Digest
from digestparser.conf import raw_config, parse_raw_config
from tests import read_fixture, test_data_path, fixture_file


class FakeResponse(object):
    def __new__(cls, json_response):
        new_instance = object.__new__(cls)
        new_instance.__init__(json_response)
        return new_instance

    def __init__(self, json_response):
        self.json_response = json_response

    def json(self):
        return self.json_response


@ddt
class TestJsonOutput(unittest.TestCase):

    def setUp(self):
        pass

    @data(
        {
            'comment': 'docx, JATS and image input data',
            'config_section': 'elife',
            'file_name': 'DIGEST 99999.zip',
            'jats_file': 'elife-99999-v0.xml',
            'image_file_name': 'digest-99999.jpg',
            'iiif_info': {'width': 800, 'height': 600},
            'related': [{
                'id': '99999',
                'type': 'research-article',
                'status': 'vor',
                'version': 1,
                'doi': '10.7554/eLife.99999',
                'authorLine': 'Anonymous et al.',
                'title': 'A research article related to the digest',
                'stage': 'published',
                'published': '2018-06-04T00:00:00Z',
                'statusDate': '2018-06-04T00:00:00Z',
                'volume': 7,
                'elocationId': 'e99999'
                }],
            'expected_json_file': 'json_content_99999.py'
        },
        {
            'comment': 'an image but no IIIF size data',
            'config_section': 'elife',
            'file_name': 'DIGEST 99999.zip',
            'image_file_name': 'digest-99999.jpg',
            'expected_json_file': 'json_content_no_iiif_99999.py'
        },
        {
            'comment': 'JSON output from a docx input only',
            'config_section': 'elife',
            'file_name': 'DIGEST 99999.docx',
            'jats_file': None,
            'image_file_name': None,
            'related': None,
            'expected_json_file': 'json_content_docx_only_99999.py'
        },
        {
            'comment': 'JSON output from a docx and JATS file only',
            'config_section': 'elife',
            'file_name': 'DIGEST 99999.docx',
            'jats_file': 'elife-99999-v0.xml',
            'image_file_name': None,
            'related': None,
            'expected_json_file': 'json_content_docx_and_jats_99999.py'
        },
        )
    @patch.object(json_output, 'iiif_server_info')
    def test_build_json(self, test_data, fake_iiif_server_info):
        "check building a JSON from a DOCX file"
        fake_iiif_server_info.return_value = test_data.get('iiif_info')
        file_name = test_data_path(test_data.get('file_name'))
        jats_file = fixture_file(test_data.get('jats_file'))
        expected_json = read_fixture(test_data.get('expected_json_file'))
        # config
        digest_config = parse_raw_config(raw_config(test_data.get('config_section')))
        image_file_name = test_data.get('image_file_name')
        related = test_data.get('related')
        # build now
        json_content = json_output.build_json(file_name, 'tmp', digest_config,
                                              jats_file, image_file_name, related)
        # assert assertions
        self.assertEqual(json_content, expected_json,
                         'failed in {comment}'.format(comment=test_data.get("comment")))

    def test_image_info_missing_data(self):
        "test missing data when requesting IIIF server info for coverage"
        self.assertEqual(json_output.image_info(None, None, None), {})

    @patch.object(json_output.requests, 'get')
    def test_iiif_server_info(self, fake_get):
        "test the iiif server connection mocking requests"
        fake_get.return_value = FakeResponse({'width': 100})
        expected_info = {'width': 100}
        self.assertEqual(json_output.iiif_server_info('http://iiif'), expected_info)

    @patch.object(json_output.requests, 'get')
    def test_iiif_server_info_error(self, fake_get):
        "test iiif server exception"
        fake_get.side_effect = RuntimeError()
        fake_get.return_value = FakeResponse({'width': 100})
        expected_info = {}
        self.assertEqual(json_output.iiif_server_info('http://iiif-error'), expected_info)

    def test_digest_json_empty(self):
        "test json output for an empty digest where there is no text or image file"
        digest = Digest()
        # reset some lists to None for testing
        digest.text = None
        digest.keywords = None
        digest.subjects = None
        expected = OrderedDict([
            ('id', 'None'),
            ('title', None),
            ('impactStatement', None),
            ('content', [])
            ])
        self.assertEqual(json_output.digest_json(digest, None), expected)


if __name__ == '__main__':
    unittest.main()
