# coding=utf-8

import unittest
from mock import patch
from digestparser.conf import raw_config, parse_raw_config
from digestparser.objects import Image, Digest
from digestparser import medium_post
from tests import read_fixture, data_path, fixture_file


class MockClient:
    "mock Medium client to use in testing"

    def __new__(cls, create_post_return=None):
        new_instance = object.__new__(cls)
        new_instance.__init__(create_post_return)
        return new_instance

    def __init__(self, create_post_return=None):
        self.access_token = None
        self.user_id = None
        self.title = None
        self.content = None
        self.content_format = None
        self.tags = None
        self.canonical_url = None
        self.publish_status = None
        self.license = None
        # default data returned
        if create_post_return is not None:
            self.create_post_return = create_post_return
        else:
            self.create_post_return = {
                "canonicalUrl": "",
                "license": "all-rights-reserved",
                "title": "My Title",
                "url": "https://medium.com/@kylehg/55050649c95",
                "tags": ["python", "is", "great"],
                "authorId": "1f86...",
                "publishStatus": "draft",
                "id": "55050649c95",
            }

    def get_current_user(self):
        return {"id": None}

    def create_post(
        self,
        user_id,
        title,
        content,
        content_format,
        tags=None,
        canonical_url=None,
        publish_status=None,
        license=None,
    ):
        "mock the create_post of the medium Client"
        # use all the variables to satisfy the linter self-use directive
        self.user_id = user_id
        self.title = title
        self.content = content
        self.content_format = content_format
        self.tags = tags
        self.canonical_url = canonical_url
        self.publish_status = publish_status
        self.license = license
        # now can return the data
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


def build_image(caption=None, file_value=None):
    "build an Image object for testing"
    image = Image()
    if caption:
        image.caption = caption
    if file_value:
        image.file = file_value
    return image


class TestMediumFigure(unittest.TestCase):
    def setUp(self):
        self.digest_config = parse_raw_config(raw_config("elife"))

    def test_digest_figure_caption_content(self):
        "test figure caption content formatting"
        image = build_image(caption="Caption. Anonymous (CC BY\xa04.0)", file_value="")
        expected = "<figcaption>Caption. Anonymous (CC BY\xa04.0)</figcaption>"
        self.assertEqual(
            medium_post.digest_figure_caption_content(self.digest_config, image),
            expected,
        )

    def test_digest_figure_image_url(self):
        "test figure image url formatting"
        image = build_image(file_value="test.jpg")
        digest = Digest()
        digest.doi = "10.7554/eLife.99999"
        expected = "https://iiif.elifesciences.org/digests/99999%2Ftest.jpg/full/full/0/default.jpg"
        self.assertEqual(
            medium_post.digest_figure_image_url(self.digest_config, image, digest),
            expected,
        )

    def test_digest_figure_content(self):
        "test figure caption formatting"
        image = build_image(
            caption="Caption. Anonymous (CC BY\xa04.0)", file_value="test.jpg"
        )
        digest = Digest()
        digest.doi = "10.7554/eLife.99999"
        expected = (
            "<figure>"
            + '<img src="https://iiif.elifesciences.org/digests/99999%2Ftest.jpg/full/full/0/default.jpg" />'
            + "<figcaption>Caption. Anonymous (CC BY\xa04.0)</figcaption></figure>"
        )
        self.assertEqual(
            medium_post.digest_figure_content(self.digest_config, image, digest),
            expected,
        )

    def test_build_medium_content(self):
        "test building from a DOCX file and converting to Medium content"
        docx_file = "DIGEST 99999.docx"
        expected_medium_content = read_fixture("medium_content_99999.py")
        # build the digest object
        medium_content = medium_post.build_medium_content(
            data_path(docx_file), "tmp", self.digest_config
        )
        # test assertions
        self.assertEqual(medium_content, expected_medium_content)

    def test_build_medium_content_with_jats(self):
        "test building from a zip file and converting to Medium content"
        docx_file = "DIGEST 99999.zip"
        jats_file = fixture_file("elife-99999-v0.xml")
        expected_medium_content = read_fixture("medium_content_jats_99999.py")
        # build the digest object
        medium_content = medium_post.build_medium_content(
            data_path(docx_file), "tmp", self.digest_config, jats_file
        )
        # test assertions
        self.assertEqual(medium_content, expected_medium_content)

    def test_build_medium_content_with_jats_and_image(self):
        "test building from a DOCX file and converting to Medium content"
        docx_file = "DIGEST 99999.docx"
        jats_file = fixture_file("elife-99999-v0.xml")
        image_file_name = "IMAGE 99999.jpeg"
        expected_medium_content = read_fixture("medium_content_jats_99999.py")
        # build the digest object
        medium_content = medium_post.build_medium_content(
            data_path(docx_file), "tmp", self.digest_config, jats_file, image_file_name
        )
        # test assertions
        self.assertEqual(medium_content, expected_medium_content)

    @patch.object(medium_post, "Client")
    def test_post_content(self, fake_client):
        "test posting content to Medium mocking the endpoint"
        fake_client.return_value = MockClient()
        medium_content = None
        # do the action
        post = medium_post.post_content(medium_content, self.digest_config)
        # test assertions
        self.assertEqual(post.get("publishStatus"), "draft")

    def test_image_formatter(self):
        "test image formatter for coverage"
        expected = "<figcaption></figcaption>"
        string = medium_post.image_formatter(
            self.digest_config, "medium_figcaption_pattern"
        )
        self.assertEqual(string, expected)


if __name__ == "__main__":
    unittest.main()
