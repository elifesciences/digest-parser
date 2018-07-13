"build JSON output from digest content"

from collections import OrderedDict
from digestparser.utils import msid_from_doi
from digestparser.jats import parse_jats_digest, xml_to_html
from digestparser.build import build_digest


def content_paragraph(text):
    "create a content paragraph from the text"
    paragraph = OrderedDict()
    paragraph['type'] = 'paragraph'
    paragraph['text'] = text
    return paragraph


def digest_json(digest, published=None):
    "convert a digest object to JSON output"
    # todo!!!
    json_content = OrderedDict()
    # id, for now use the msid from the doi
    json_content['id'] = str(msid_from_doi(digest.doi))
    json_content['title'] = digest.title
    json_content['impactStatement'] = digest.summary
    # published date todo!!!
    json_content['published'] = str(published)
    # image todo!!!
    json_content['image'] = OrderedDict()
    # subjects todo!!
    subjects = []
    subjects.append(OrderedDict())
    json_content['subjects'] = subjects
    # content
    content = []
    for text in digest.text:
        content.append(content_paragraph(text))
    json_content['content'] = content
    # related content todo!!!
    json_content['relatedContent'] = OrderedDict()
    return json_content


def build_json(file_name, jats_file_name=None):
    "build JSON output from a DOCX input file and possibly some JATS input"
    digest = build_digest(file_name)

    # override the text with the jats file digest content
    if jats_file_name:
        jats_content = parse_jats_digest(jats_file_name)
        if jats_content:
            digest.text = map(xml_to_html, jats_content)

    json_content = digest_json(digest)

    # add the subjects from the jats file
    # todo!!!

    return json_content
