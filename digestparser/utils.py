"utility helper functions"
import re


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
