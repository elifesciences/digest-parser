# coding=utf-8

import unittest
from mock import patch
from digestparser.conf import raw_config, parse_raw_config
from digestparser.objects import Image
from digestparser import medium_post
from tests import read_fixture, test_data_path, fixture_file


class MockClient():
    "mock Medium client to use in testing"
    def __init__(self, create_post_return=None):
        self.access_token = None
        # default data returned
        if create_post_return is not None:
            self.create_post_return=create_post_return
        else:
            self.create_post_return = {
                'canonicalUrl': '',
                'license': 'all-rights-reserved',
                'title': 'My Title',
                'url': 'https://medium.com/@kylehg/55050649c95',
                'tags': ['python', 'is', 'great'],
                'authorId': '1f86...',
                'publishStatus': 'draft',
                'id': '55050649c95'
                }

    def get_current_user(self):
        user = {}
        user['id'] = None
        return user

    def create_post(self, user_id, title, content, content_format, tags=None,
                    canonical_url=None, publish_status=None, license=None):
        return self.create_post_return


class TestMockClient(unittest.TestCase):
    "test the mock client for coverage"
    def test_mock_client(self):
        create_post_return = {}
        user_id = None
        title = None
        content = None
        content_format = None
        # create the client
        fake_client = MockClient(create_post_return)
        # test assertions
        post = fake_client.create_post(user_id, title, content, content_format)
        self.assertEqual(post, create_post_return)


class TestMedium(unittest.TestCase):

    def setUp(self):
        self.digest_config = parse_raw_config(raw_config('elife'))

    def build_image(self, caption=None, credit=None, license_value=None, file_value=None):
        "build an Image object for testing"
        image = Image()
        if caption:
            image.caption = caption
        if credit:
            image.credit = credit
        if license_value:
            image.license = license_value
        if file_value:
            image.file = file_value
        return image

    def test_digest_figure_license(self):
        "test figure license content formatting"
        image = self.build_image(license_value=u'CC BY\xa04.0')
        expected = u' (CC BY\xa04.0)'
        self.assertEqual(medium_post.digest_figure_license(self.digest_config, image), expected)

    def test_digest_figure_caption_content(self):
        "test figure caption content formatting"
        image = self.build_image(
            caption='Caption.', credit='Anonymous', license_value=u'CC BY\xa04.0', file_value='')
        expected = u'<figcaption>Caption. Anonymous (CC BY\xa04.0)</figcaption>'
        self.assertEqual(medium_post.digest_figure_caption_content(
            self.digest_config, image), expected)

    def test_digest_figure_image_url(self):
        "test figure image url formatting"
        image = self.build_image(file_value='test.jpg')
        expected = u'https://cdn.elifesciences.org/medium_test/test.jpg'
        self.assertEqual(medium_post.digest_figure_image_url(
            self.digest_config, image), expected)

    def test_digest_figure_content(self):
        "test figure caption formatting"
        image = self.build_image(
            caption='Caption.', credit='Anonymous', license_value=u'CC BY\xa04.0', file_value='test.jpg')
        expected = u'<figure><img src="https://cdn.elifesciences.org/medium_test/test.jpg" /><figcaption>Caption. Anonymous (CC BY\xa04.0)</figcaption></figure>'
        self.assertEqual(medium_post.digest_figure_content(
            self.digest_config, image), expected)

    def test_build_medium_content(self):
        "test building from a DOCX file and converting to Medium content"
        config_section = 'elife'
        docx_file = 'DIGEST 99999.docx'
        expected_medium_content = read_fixture('medium_content_99999.py')
        # build the digest object
        medium_content = medium_post.build_medium_content(test_data_path(docx_file), config_section)
        # test assertions
        self.assertEqual(medium_content, expected_medium_content)


    def test_build_medium_content_with_jats(self):
        "test building from a DOCX file and converting to Medium content"
        config_section = 'elife'
        docx_file = 'DIGEST 99999.zip'
        jats_file = fixture_file('elife-99999-v0.xml')
        expected_medium_content = read_fixture('medium_content_jats_99999.py')
        # build the digest object
        medium_content = medium_post.build_medium_content(
            test_data_path(docx_file), config_section, jats_file)
        # test assertions
        self.assertEqual(medium_content, expected_medium_content)


    @patch.object(medium_post, 'Client')
    def test_post_content(self, fake_client):
        "test posting content to Medium mocking the endpoint"
        fake_client.return_value = MockClient()
        config_section = 'elife'
        medium_content = {}
        # do the action
        post = medium_post.post_content(medium_content)
        # test assertions
        self.assertEqual(post.get('publishStatus'), 'draft')



if __name__ == '__main__':
    unittest.main()
