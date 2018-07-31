"build JSON output from digest content"
import os
import copy
from collections import OrderedDict
from digestparser.utils import msid_from_doi
from digestparser.jats import parse_jats_digest, xml_to_html
from digestparser.build import build_digest
from digestparser.conf import raw_config, parse_raw_config


def image_info(msid, file_name):
    "get image info from the IIIF server"
    if not msid or not file_name:
        return {}
    # todo logic for requests to IIIF server
    return {}


def image_attribution(credit, image_license):
    "concatenate an image attribution"
    attribution = []
    attribution_line = ', '.join([part for part in credit, image_license if part])
    attribution.append(attribution_line)
    return attribution


def image_uri(msid, file_name, digest_config):
    "uri of the image file as defined in the settings"
    return digest_config.get('iiif_image_uri').format(msid=msid, file_name=file_name)


def image_source(msid, file_name, digest_config):
    "source of the iiif image as defined in the settings"
    source = OrderedDict()
    source['mediaType'] = "image/jpeg"
    source['uri'] = digest_config.get('iiif_image_source_uri').format(msid=msid,
                                                                      file_name=file_name)
    source['filename'] = file_name
    return source


def image_size(info):
    "size of the iiif image from the info"
    size = OrderedDict()
    # todo - get the size from the json
    size['width'] = info.get('width')
    size['height'] = info.get('height')
    return size


def image_json(digest, digest_config):
    "format image details into JSON format"
    msid = str(msid_from_doi(digest.doi))
    image_file_name = os.path.split(digest.image.file)[-1]
    image = OrderedDict()
    image['type'] = 'image'
    # image details
    image_details = OrderedDict()
    # medium_image_url
    image_details['uri'] = image_uri(msid, image_file_name, digest_config)
    image_details['alt'] = ''
    attribution = image_attribution(digest.image.credit, digest.image.license)
    if attribution:
        image_details['attribution'] = attribution
    source = image_source(msid, image_file_name, digest_config)
    image_details['source'] = source
    # populate with IIIF server data
    info = image_info(msid, digest.image.file)
    size = image_size(info)
    image_details['size'] = size
    image['image'] = image_details
    image['title'] = digest.image.caption
    return image


def thumbnail_image_from_image_json(image_json):
    "modify the image_json to an image thumbnail image format"
    thumbnail_image_json = copy.deepcopy(image_json)
    # delete some data
    del thumbnail_image_json['type']
    del thumbnail_image_json['title']
    if thumbnail_image_json['image'].get('attribution'):
        del thumbnail_image_json['image']['attribution']
    # change the index name
    thumbnail_image_json['thumbnail'] = thumbnail_image_json['image']
    del thumbnail_image_json['image']
    return thumbnail_image_json


def content_paragraph(text):
    "create a content paragraph from the text"
    paragraph = OrderedDict()
    paragraph['type'] = 'paragraph'
    paragraph['text'] = text
    return paragraph


def digest_json(digest, digest_config, published=None):
    "convert a digest object to JSON output"
    json_content = OrderedDict()
    # id, for now use the msid from the doi
    json_content['id'] = str(msid_from_doi(digest.doi))
    json_content['title'] = digest.title
    json_content['impactStatement'] = digest.summary
    # published date todo!!!
    json_content['published'] = str(published)
    # image todo!!!
    content_image = image_json(digest, digest_config)
    thumbnail_image = thumbnail_image_from_image_json(content_image)
    json_content['image'] = thumbnail_image
    # subjects todo!!
    subjects = []
    subjects.append(OrderedDict())
    json_content['subjects'] = subjects
    # content
    content = []
    if content_image:
        content.append(content_image)
    for text in digest.text:
        content.append(content_paragraph(text))
    json_content['content'] = content
    # related content todo!!!
    json_content['relatedContent'] = OrderedDict()
    return json_content


def build_json(file_name, config_section=None, jats_file_name=None):
    "build JSON output from a DOCX input file and possibly some JATS input"
    digest_config = parse_raw_config(raw_config(config_section))
    digest = build_digest(file_name)

    # override the text with the jats file digest content
    if jats_file_name:
        jats_content = parse_jats_digest(jats_file_name)
        if jats_content:
            digest.text = map(xml_to_html, jats_content)

    json_content = digest_json(digest, digest_config)

    # add the subjects from the jats file
    # todo!!!

    return json_content
