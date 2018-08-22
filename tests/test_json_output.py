# coding=utf-8

import unittest
from mock import patch
from ddt import ddt, data
from digestparser import json_output
from digestparser.conf import raw_config, parse_raw_config
from tests import read_fixture, test_data_path, fixture_file


@ddt
class TestJsonOutput(unittest.TestCase):

    def setUp(self):
        pass

    @data(
        {
            'config_section': 'elife',
            'file_name': 'DIGEST 99999.zip',
            'jats_file': 'elife-99999-v0.xml',
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
        )
    @patch.object(json_output, 'image_info')
    def test_build_json(self, test_data, fake_image_info):
        "check building a JSON from a DOCX file"
        fake_image_info.return_value = {'width': 0, 'height': 0}
        config_section = 'elife'
        file_name = test_data_path(test_data.get('file_name'))
        jats_file = fixture_file(test_data.get('jats_file'))
        expected_json = read_fixture(test_data.get('expected_json_file'))
        # config
        digest_config = parse_raw_config(raw_config(test_data.get('config_section')))
        related = test_data.get('related')
        # build now
        json_content = json_output.build_json(file_name, 'tmp', digest_config, jats_file, related)
        # assert assertions
        #import json
        #print(json.dumps(json_content, indent=4))
        #print(json.dumps(expected_json, indent=4))
        self.assertEqual(json_content, expected_json)

    def test_image_info_missing_data(self):
        "test missing data when requesting IIIF server info for coverage"
        self.assertEqual(json_output.image_info(None, None), {})


if __name__ == '__main__':
    unittest.main()
