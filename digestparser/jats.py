"build JATS XML output from digest content"

from collections import OrderedDict
from elifetools import parseJATS as parser
from elifetools.utils import (
    escape_unmatched_angle_brackets,
    escape_ampersand,
    subject_slug,
)
from elifetools.utils_html import replace_simple_tags
from digestparser.build import build_digest


def allowed_xml_tag_fragments():
    """
    tuples of whitelisted tag startswith values for matching tags found in inline text
    prior to being converted to HTML
    values can be a complete tag for exact matching just the first few characters of a tag
    such as the case would be for mml: or table td tags
    """
    return (
        "<italic>",
        "</italic>",
        "<italic/>",
        "<bold>",
        "</bold>",
        "<bold/>",
        "<i>",
        "</i>",
        "<i/>",
        "<b>",
        "</b>",
        "<b/>",
        "<sub>",
        "</sub>",
        "<sub/>",
        "<sup>",
        "</sup>",
        "<sup/>",
    )


def escape_xml(xml_string):
    "escape ampersands and unmatched angle brackets in HTML string allowing some whitelisted tags"
    xml_string = escape_ampersand(xml_string)
    return escape_unmatched_angle_brackets(xml_string, allowed_xml_tag_fragments())


def html_to_xml(html_string):
    "convert HTML style content to XML style tagging with escaped special characters"
    xml_string = html_string
    xml_string = replace_simple_tags(xml_string, "i", "italic")
    xml_string = replace_simple_tags(xml_string, "b", "bold")
    # note: sub and sup tags are valid in HTML and XML so do not need to be replaced
    xml_string = escape_xml(xml_string)
    return xml_string


def xml_to_html(xml_string):
    "convert XML style content to HTML style tagging"
    html_string = xml_string
    html_string = replace_simple_tags(html_string, "italic", "i")
    html_string = replace_simple_tags(html_string, "bold", "b")
    html_string = escape_xml(html_string)
    return html_string


def digest_jats(digest):
    "convert a digest object to JATS XML output"
    jats_content = u""
    # convert text into paragraphs converting inline HTML tags
    for text in [text.strip() for text in digest.text if text and text.strip()]:
        jats_content += "<p>" + html_to_xml(text) + "</p>"
    return jats_content


def split_paragraphs(string):
    "split a string with paragraph tags into a list of lines"
    if not string:
        return string
    content = []
    for snippet in string.split("<p>"):
        clean_snippet = snippet.rstrip()
        if clean_snippet.endswith("</p>"):
            clean_snippet = "".join(clean_snippet.split("</p>")[0:-1])
        if clean_snippet != "":
            content.append(clean_snippet)
    return content


def parse_jats_file(jats_file_name):
    "parse the jats file into a BeautifulSoup object"
    return parser.parse_document(jats_file_name)


def parse_jats_digest(soup):
    "extract the digest paragraphs from soup"
    jats_digest = parser.full_digest(soup)
    return split_paragraphs(jats_digest)


def parse_jats_pub_date(soup):
    "extract the pub date from the soup"
    pub_date = parser.pub_date(soup)
    return pub_date


def parse_jats_subjects(soup):
    "extract the subject categories from the soup and format them as json"
    subjects = []
    categories = parser.category(soup)
    for category in categories:
        subject = OrderedDict()
        subject["id"] = subject_slug(category)
        subject["name"] = category
        subjects.append(subject)
    return subjects


def build_jats(file_name, temp_dir="tmp", digest_config=None):
    "build a digest object from a DOCX input file"
    digest = build_digest(file_name, temp_dir, digest_config)
    jats_content = digest_jats(digest)
    return jats_content
