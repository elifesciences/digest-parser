"compose a Medium post from digest content"

from collections import OrderedDict
from digestparser.build import build_digest
from digestparser.html import string_to_html
from digestparser.conf import raw_config, parse_raw_config

def digest_medium_title(digest):
    "extract converted Medium title from a digest object"
    return string_to_html(digest.title)


def digest_formatter(digest_config, format_name, digest, content={}):
    "take a format from the config file and convert it to a string using digest attributes"
    string = u''
    if digest_config.get(format_name):
        string = digest_config.get(format_name).format(
            digest_title=string_to_html(digest.title),
            digest_summary=string_to_html(digest.summary),
            digest_doi=digest.doi,
            text=string_to_html(content.get('text')),
            title=content.get('title'),
            summary=content.get('summary'),
            body=content.get('body'),
            footer=content.get('footer'))
    return string


def digest_medium_content(digest, digest_config={}):
    "extract converted Medium content from a digest object"
    # title
    title = digest_formatter(digest_config, 'medium_title_format', digest)
    # summary
    summary = digest_formatter(digest_config, 'medium_summary_format', digest)
    # body
    body = u''
    for text in digest.text:
        content = {'text': text}
        # convert text into paragraphs converting inline HTML tags
        body += digest_formatter(digest_config, 'medium_paragraph_format', digest, content)
    # footer
    footer = digest_formatter(digest_config, 'medium_footer_format', digest)
    # format the final content medium_content
    content = {
        'title': title,
        'summary': summary,
        'body': body,
        'footer': footer,
        }
    medium_content = digest_formatter(digest_config, 'medium_content_format', digest, content)
    return medium_content


def digest_medium_tags(digest):
    "extract converted Medium tags from a digest object"
    return digest.keywords


def digest_medium_license(digest, digest_config={}):
    "set the medium license"
    medium_license = None
    if digest_config.get('medium_license'):
        medium_license = digest_config.get('medium_license')
    return medium_license


def build_medium_content(file_name, config_section=None):
    "build Medium content from a DOCX input file"
    digest_config = parse_raw_config(raw_config(config_section))

    content_format = 'html'

    # build the digest object
    digest = build_digest(file_name)

    # convert to Medium content components
    title = digest_medium_title(digest)
    # todo!! pass in footer content
    content = digest_medium_content(digest, digest_config)
    tags = digest_medium_tags(digest)
    # license
    medium_license = digest_medium_license(digest, digest_config)

    # assemble the return value
    medium_content = OrderedDict()
    medium_content['title'] = title
    medium_content['contentFormat'] = content_format
    medium_content['content'] = content
    if tags:
        medium_content['tags'] = tags
    if medium_license:
        medium_content['license'] = medium_license
    return medium_content
