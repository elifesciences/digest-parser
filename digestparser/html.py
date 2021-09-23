"convert parsed content to HTML"

from elifetools.utils import escape_unmatched_angle_brackets, escape_ampersand


def allowed_xml_tag_fragments():
    """
    tuples of whitelisted tag startswith values for matching tags found in inline text
    prior to being converted to HTML
    values can be a complete tag for exact matching just the first few characters of a tag
    such as the case would be for mml: or table td tags
    """
    return (
        '<i>', '</i>', '<i/>',
        '<b>', '</b>', '<b/>',
        '<sub>', '</sub>', '<sub/>',
        '<sup>', '</sup>', '<sup/>',
        )


def escape_html(html_string):
    "escape ampersands and unmatched angle brackets in HTML string allowing some whitelisted tags"
    html_string = escape_ampersand(html_string)
    return escape_unmatched_angle_brackets(html_string, allowed_xml_tag_fragments())


def string_to_html(string):
    "convert HTML-like content parsed from DOCX into fully escaped HTML"
    html_string = string
    # note: b, i, sub and sup tags are valid in HTML and XML so do not need to be replaced
    html_string = escape_html(html_string)
    return html_string
