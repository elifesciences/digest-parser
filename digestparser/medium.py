"compose a Medium post from digest content"

from collections import OrderedDict
from digestparser.build import build_digest
from digestparser.html import string_to_html


def digest_medium_title(digest):
    "extract converted Medium title from a digest object"
    return string_to_html(digest.title)


def digest_medium_content(digest, footer=''):
    "extract converted Medium content from a digest object"
    # todo!! formatting
    medium_content = u''
    # title
    medium_content += u'<h1>{title}</h1>'.format(title=string_to_html(digest.title))
    # summary
    medium_content += u'<h1>{summary}</h1>'.format(summary=string_to_html(digest.summary))
    # section / divider
    medium_content += u'<hr/>'
    # content
    for text in digest.text:
        # convert text into paragraphs converting inline HTML tags
        medium_content += u'<p>{text}</p>'.format(text=string_to_html(text))
    # footer
    medium_content += footer
    return medium_content


def digest_medium_tags(digest):
    "extract converted Medium tags from a digest object"
    return digest.keywords


def build_medium_content(file_name):
    "build Medium content from a DOCX input file"
    # todo - specify alternate license
    medium_license = 'cc-40-by'
    content_format = 'html'

    # build the digest object
    digest = build_digest(file_name)

    # convert to Medium content components
    title = digest_medium_title(digest)
    # todo!! pass in footer content
    content = digest_medium_content(digest)
    tags = digest_medium_tags(digest)

    # assemble the return value
    medium_content = OrderedDict()
    medium_content['title'] = title
    medium_content['contentFormat'] = content_format
    medium_content['content'] = content
    medium_content['tags'] = tags
    medium_content['license'] = medium_license
    return medium_content
