# coding=utf-8

"utility helper functions"
import re


def sanitise(file_name):
    "replace unwanted characters in file name if present"
    if not file_name:
        return file_name
    file_name = file_name.replace("/", "")
    file_name = file_name.replace("\\", "")
    file_name = re.sub(r"\.+", ".", file_name)
    file_name = file_name.lstrip(".")
    return file_name


def char_map():
    "set of character replacements for use in sanitising file names"
    return {
        u"’": "'",
        u"‘": "'",
        u"“": '"',
        u"”": '"',
    }


def sanitise_file_name(file_name):
    "more extensive sanitising of a file name with some replacement characters and allowed ones"
    # basic sanitise first
    file_name = sanitise(file_name)
    # character replacements
    for match, replacement in char_map().items():
        file_name = re.sub(match, replacement, file_name)
    # remove more unsafe impossible file name characters
    file_name = re.sub(r'[*:"<>|]', "", file_name)
    return file_name


def formatter_string(content, attribute):
    "return blank string if None or content attribute does not exist"
    if not content:
        return ""
    return content.get(attribute) if content.get(attribute) else ""


def msid_from_doi(doi):
    "return just the article id portion of an eLife doi as an integer"
    if not doi:
        return
    if not isinstance(doi, str):
        return
    regex = r"10\.7554/elife\.(?P<msid>\d+)"
    match_list = re.findall(regex, doi, re.IGNORECASE)
    if len(match_list) > 0:
        return int(match_list[0])
