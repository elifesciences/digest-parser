"build JATS XML output from digest content"

from digestparser.build import build_digest
from elifetools.utils import escape_unmatched_angle_brackets, escape_ampersand
from elifetools.utils_html import replace_simple_tags

def allowed_xml_tag_fragments():
    """
    tuples of whitelisted tag startswith values for matching tags found in inline text
    prior to being converted to HTML
    values can be a complete tag for exact matching just the first few characters of a tag
    such as the case would be for mml: or table td tags
    """
    return (
        '<italic>', '</italic>','<italic/>',
        '<bold>', '</bold>', '<bold/>',
        '<underline>', '</underline>', '<underline/>',
        '<sub>', '</sub>', '<sub/>',
        '<sup>', '</sup>', '<sup/>',
        )


def escape_xml(xml_string):
    "escape ampersands and unmatched angle brackets in HTML string allowing some whitelisted tags"
    xml_string = escape_ampersand(xml_string)
    return escape_unmatched_angle_brackets(xml_string, allowed_xml_tag_fragments())


def html_to_xml(html_string):
    "convert HTML style content to XML style tagging with escaped special characters"
    xml_string = html_string
    xml_string = replace_simple_tags(xml_string, 'i', 'italic')
    xml_string = replace_simple_tags(xml_string, 'b', 'bold')
    xml_string = replace_simple_tags(xml_string, 'u', 'underline')
    # note: sub and sup tags are valid in HTML and XML so do not need to be replaced
    xml_string = escape_xml(xml_string)
    return xml_string


def digest_jats(digest):
    "convert a digest object to JATS XML output"
    jats_content = u''
    # convert text into paragraphs converting inline HTML tags
    for text in digest.text:
        jats_content += '<p>' + html_to_xml(text) + '</p>'
    return jats_content


def build_jats(file_name):
    "build a digest object from a DOCX input file"
    digest = build_digest(file_name)
    jats_content = digest_jats(digest)
    return jats_content
