"utility helper functions"
import re
import urllib
from slugify import slugify


def sanitise(file_name):
    "replace unwanted characters in file name if present"
    if not file_name:
        return file_name
    file_name = file_name.replace('/', '')
    file_name = file_name.replace('\\', '')
    file_name = re.sub(r'\.+', '.', file_name)
    file_name = file_name.lstrip('.')
    return file_name


def formatter_string(content, attribute):
    "return blank string if None or content attribute does not exist"
    if not content:
        return ''
    return content.get(attribute) if content.get(attribute) else ''


def msid_from_doi(doi):
    "return just the id portion of the doi"
    try:
        msid = int(doi.split(".")[-1])
    except (AttributeError, ValueError, IndexError):
        msid = None
    return msid


def url_quote(string):
    "escape for url quoting with python 2 or 3 method"
    if hasattr(urllib, 'parse'):
        # python 3
        return urllib.parse.quote(string)
    return urllib.quote(string)


def subject_slug(subject):
    "create a slug for a subject value"
    return slugify(subject, stopwords=['and', 'of'])
