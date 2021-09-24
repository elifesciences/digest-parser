"compose a Medium post from digest content"

import os
import urllib
from collections import OrderedDict
from medium import Client
from digestparser import utils
from digestparser.build import build_digest
from digestparser.jats import parse_jats_file, parse_jats_digest, xml_to_html
from digestparser.html import string_to_html


def digest_medium_title(digest):
    "extract converted Medium title from a digest object"
    return string_to_html(digest.title)


def digest_formatter(digest_config, format_name, digest, content=None):
    "take a format from the config file and convert it to a string using digest attributes"
    string = u""
    if digest_config.get(format_name):
        string = digest_config.get(format_name).format(
            digest_title=string_to_html(digest.title),
            digest_summary=string_to_html(digest.summary),
            digest_doi=digest.doi,
            text=string_to_html(utils.formatter_string(content, "text")),
            title=utils.formatter_string(content, "title"),
            summary=utils.formatter_string(content, "summary"),
            body=utils.formatter_string(content, "body"),
            footer=utils.formatter_string(content, "footer"),
            figure=utils.formatter_string(content, "figure"),
            msid=utils.msid_from_doi(digest.doi),
        )
    return string


def image_formatter(digest_config, format_name, content=None):
    "take a format from the config file and convert it to a string using image attributes"
    string = u""
    if digest_config.get(format_name):
        string = digest_config.get(format_name).format(
            image_url=utils.formatter_string(content, "image_url"),
            figcaption=utils.formatter_string(content, "figcaption"),
            caption=utils.formatter_string(content, "caption"),
            file_name=urllib.parse.quote(utils.formatter_string(content, "file_name")),
            msid=utils.formatter_string(content, "msid"),
        )
    return string


def digest_figure_caption_content(digest_config, image):
    "figure caption based on the pattern in the config file"
    content = {"caption": image.caption}
    return image_formatter(digest_config, "medium_figcaption_pattern", content)


def digest_figure_image_url(digest_config, image, digest):
    "image url based on the image object file attribute"
    content = {
        "file_name": os.path.split(image.file)[-1],
        "msid": utils.msid_from_doi(digest.doi),
    }
    return image_formatter(digest_config, "medium_image_url", content)


def digest_figure_content(digest_config, image, digest):
    "create figure content from the image object using the formatting in the config"
    content = {
        "image_url": digest_figure_image_url(digest_config, image, digest),
        "figcaption": digest_figure_caption_content(digest_config, image),
    }
    return image_formatter(digest_config, "medium_figure_pattern", content)


def digest_medium_content(digest, digest_config=None):
    "extract converted Medium content from a digest object"
    # title
    title = digest_formatter(digest_config, "medium_title_pattern", digest)
    # summary
    summary = digest_formatter(digest_config, "medium_summary_pattern", digest)
    # body
    body = u""
    for text in digest.text:
        content = {"text": text}
        # convert text into paragraphs converting inline HTML tags
        body += digest_formatter(
            digest_config, "medium_paragraph_pattern", digest, content
        )
    # footer
    footer = digest_formatter(digest_config, "medium_footer_pattern", digest)
    # figure
    figure = u""
    if digest.image and digest.image.file:
        figure = digest_figure_content(digest_config, digest.image, digest)
    # format the final content medium_content
    content = {
        "figure": figure,
        "title": title,
        "summary": summary,
        "body": body,
        "footer": footer,
    }
    medium_content = digest_formatter(
        digest_config, "medium_content_pattern", digest, content
    )
    return medium_content


def digest_medium_tags(digest):
    "extract converted Medium tags from a digest object"
    return digest.keywords


def digest_medium_license(digest_config):
    "set the medium license"
    medium_license = None
    if digest_config and digest_config.get("medium_license"):
        medium_license = digest_config.get("medium_license")
    return medium_license


def digest_medium_content_format(digest_config):
    "set the medium content format, typically html, or could be markdown"
    content_format = None
    if digest_config and digest_config.get("medium_content_format"):
        content_format = digest_config.get("medium_content_format")
    return content_format


def build_medium_content(
    file_name,
    temp_dir="tmp",
    digest_config=None,
    jats_file_name=None,
    image_file_name=None,
):
    "build Medium content from a DOCX input file"

    # build the digest object
    digest = build_digest(file_name, temp_dir, digest_config, image_file_name)

    # override the text with the jats file digest content
    if jats_file_name:
        soup = parse_jats_file(jats_file_name)
        jats_content = parse_jats_digest(soup)
        if jats_content:
            digest.text = map(xml_to_html, jats_content)

    # convert to Medium content components
    title = digest_medium_title(digest)
    # todo!! pass in footer content
    content_format = digest_medium_content_format(digest_config)
    content = digest_medium_content(digest, digest_config)
    tags = digest_medium_tags(digest)
    # license
    medium_license = digest_medium_license(digest_config)

    # assemble the return value
    medium_content = OrderedDict()
    medium_content["title"] = title
    medium_content["contentFormat"] = content_format
    medium_content["content"] = content
    if tags:
        medium_content["tags"] = tags
    if medium_license:
        medium_content["license"] = medium_license
    return medium_content


def post_content(medium_content, digest_config=None):
    "post the Medium content to Medium"
    medium_client = Client(
        application_id=digest_config.get("medium_application_client_id"),
        application_secret=digest_config.get("medium_application_client_secret"),
    )
    medium_client.access_token = digest_config.get("medium_access_token")
    medium_user = medium_client.get_current_user()
    # Set some optional post values
    publish_status = "draft"
    medium_license = digest_config.get("medium_license", None)

    # Create a draft post
    post = medium_client.create_post(
        user_id=medium_user["id"],
        title=utils.formatter_string(medium_content, "title"),
        content=utils.formatter_string(medium_content, "content"),
        content_format=utils.formatter_string(medium_content, "contentFormat"),
        tags=utils.formatter_string(medium_content, "tags"),
        publish_status=publish_status,
        license=medium_license,
    )
    return post


if __name__ == "__main__":
    # test while developing
    CONFIG_SECTION = "elife"
    # file_name = 'tests/test_data/DIGEST 99999.docx'
    FILE_NAME = "tests/test_data/DIGEST 99999.zip"
    MEDIUM_CONTENT = build_medium_content(FILE_NAME, CONFIG_SECTION)
    post_content(MEDIUM_CONTENT, CONFIG_SECTION)
