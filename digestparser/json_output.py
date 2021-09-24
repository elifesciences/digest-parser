"build JSON output from digest content"
import os
import copy
from collections import OrderedDict
import requests
from elifetools.utils import copy_attribute
from digestparser.utils import formatter_string, msid_from_doi
from digestparser.jats import (
    parse_jats_file,
    parse_jats_digest,
    parse_jats_subjects,
    xml_to_html,
)
from digestparser.build import build_digest
from digestparser import LOGGER


def iiif_server_info(info_url):
    "get the image info from the IIIF server"
    info = {}
    if not info_url:
        return info
    try:
        LOGGER.info("Loading IIIF info: %s", info_url)
        response = requests.get(info_url)
        info = response.json()
        LOGGER.info("IIIF info for %s: %s", info_url, info)
    except Exception as exception:
        # could be any error right now
        LOGGER.exception(
            "Exception in iiif_server_info for GET %s. Details: %s",
            info_url,
            str(exception),
        )
    return info


def image_info(msid, file_name, digest_config):
    "get image info from the IIIF server"
    info_url = formatter_string(digest_config, "iiif_info_url").format(
        msid=msid, file_name=file_name
    )
    return iiif_server_info(info_url)


def image_uri(msid, file_name, digest_config):
    "uri of the image file as defined in the settings"
    return digest_config.get("iiif_image_uri").format(msid=msid, file_name=file_name)


def image_source(msid, file_name, digest_config):
    "source of the iiif image as defined in the settings"
    source = OrderedDict()
    source["mediaType"] = "image/jpeg"
    source["uri"] = digest_config.get("iiif_image_source_uri").format(
        msid=msid, file_name=file_name
    )
    source["filename"] = file_name
    return source


def image_size(info):
    "size of the iiif image from the info"
    size = OrderedDict()
    for dimension in ["width", "height"]:
        copy_attribute(info, dimension, size)
    # only return size if it is non-empty
    if size:
        return size
    return None


def image_json(digest, digest_config):
    "format image details into JSON format"
    # need an image file name to continue
    if not digest.image or not digest.image.file:
        return None
    msid = str(msid_from_doi(digest.doi))
    image_file_name = os.path.split(digest.image.file)[-1]
    image = OrderedDict()
    image["type"] = "image"
    # image details
    image_details = OrderedDict()
    # medium_image_url
    image_details["uri"] = image_uri(msid, image_file_name, digest_config)
    image_details["alt"] = ""
    source = image_source(msid, image_file_name, digest_config)
    image_details["source"] = source
    # populate with IIIF server data
    info = image_info(msid, image_file_name, digest_config)
    size = image_size(info)
    if size:
        image_details["size"] = size
    image["image"] = image_details
    if digest.image.caption:
        image["caption"] = [(content_paragraph(digest.image.caption))]
    return image


def thumbnail_image_from_image_json(image_json):
    "modify the image_json to an image thumbnail image format"
    thumbnail_image_json = copy.deepcopy(image_json)
    # delete some data
    del thumbnail_image_json["type"]
    del thumbnail_image_json["caption"]
    # change the index name
    thumbnail_image_json["thumbnail"] = thumbnail_image_json["image"]
    del thumbnail_image_json["image"]
    return thumbnail_image_json


def content_paragraph(text):
    "create a content paragraph from the text"
    paragraph = OrderedDict()
    paragraph["type"] = "paragraph"
    paragraph["text"] = xml_to_html(text)
    return paragraph


def related_content(related):
    "format relatedContent values from a list of data"
    content = []
    values = [
        "type",
        "status",
        "id",
        "version",
        "doi",
        "authorLine",
        "title",
        "stage",
        "published",
        "statusDate",
        "volume",
        "elocationId",
    ]
    if related:
        for item in related:
            related_item = OrderedDict()
            for value in values:
                copy_attribute(item, value, related_item)
            content.append(related_item)
    return content


def digest_json(digest, digest_config, related=None):
    "convert a digest object to JSON output"
    json_content = OrderedDict()
    # id, for now use the msid from the doi
    json_content["id"] = str(msid_from_doi(digest.doi))
    json_content["title"] = digest.title
    json_content["impactStatement"] = digest.summary
    # published date
    if digest.published:
        json_content["published"] = str(digest.published)
    # image
    content_image = image_json(digest, digest_config)
    if content_image:
        thumbnail_image = thumbnail_image_from_image_json(content_image)
        json_content["image"] = thumbnail_image
    # subjects
    if digest.subjects:
        json_content["subjects"] = digest.subjects
    # content
    content = []
    if digest.text:
        for text in digest.text:
            content.append(content_paragraph(text))
    # insert the image before the first paragraph
    if content_image:
        content.insert(0, content_image)
    json_content["content"] = content
    # related content
    if related is not None:
        json_content["relatedContent"] = related_content(related)
    return json_content


def build_json(
    file_name,
    temp_dir="tmp",
    digest_config=None,
    jats_file_name=None,
    image_file_name=None,
    related=None,
):
    "build JSON output from a DOCX input file and possibly some JATS input"
    digest = build_digest(file_name, temp_dir, digest_config)

    # override the text and other details with the jats file digest content
    if jats_file_name:
        soup = parse_jats_file(jats_file_name)
        digest.text = parse_jats_digest(soup)

        # add subjects from the jats file
        digest.subjects = parse_jats_subjects(soup)

    # override the image file name if provided
    if image_file_name:
        digest.image.file = image_file_name

    json_content = digest_json(digest, digest_config, related)

    return json_content
