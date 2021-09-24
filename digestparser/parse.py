import sys
from docx import Document


# character constants
LINE_SEPARATOR = u"\u2028"


def parse_content(file_name):
    "return all the content for testing"
    document = Document(file_name)
    return parse_paragraphs(document)


def parse_paragraphs(document):
    """join the parsed paragraphs from the document"""
    content = ""
    for para in document.paragraphs:
        content += join_runs(para.runs) + "\n"
    return content


def html_open_tag(style):
    "for the style return the HTML open tag"
    style_map = {
        "italic": "<i>",
        "bold": "<b>",
        "subscript": "<sub>",
        "superscript": "<sup>",
    }
    return style_map.get(style)


def html_close_tag(style):
    "for the style return the HTML close tag"
    style_map = {
        "italic": "</i>",
        "bold": "</b>",
        "subscript": "</sub>",
        "superscript": "</sup>",
    }
    return style_map.get(style)


def html_open_close_tag(style):
    "return the HTML open and close tags for the style"
    return html_open_tag(style), html_close_tag(style)


def run_contains_break(run):
    "check if a document run contains a new line character"
    return bool(run.text.endswith("\n") if run is not None else False)


def run_has_attr(run, attribute):
    "check if a run has an attribute, for checking bold or italic for example"
    if not run:
        return None
    try:
        return getattr(run, attribute)
    except AttributeError:
        # look at the font attribute if an AttributeError is thrown
        return getattr(run.font, attribute)


def open_close_style(one_has_attr, two_has_attr, one_contains_break, output, attribute):
    "open and close tags to include between two strings based on their attributes"
    open_tag, close_tag = html_open_close_tag(style=attribute)
    if not open_tag or not close_tag:
        return output
    # add the close tag first
    if (one_has_attr and one_contains_break) or (
        one_has_attr and two_has_attr is not True
    ):
        # check for new line
        if output.endswith("\n"):
            output = output.rstrip("\n") + close_tag + "\n"
        # check for font styles extending into whitespace
        elif output.endswith(" "):
            output = output.rstrip(" ") + close_tag + " "
        else:
            output += close_tag
    # add the open tag
    if (two_has_attr and one_contains_break) or (
        two_has_attr and one_has_attr is not True
    ):
        output += open_tag
    return output


def run_open_close_style(run, prev_run, output, attribute):
    "open and close tags to include between runs"
    # extract run object data for the more general purpose function
    return open_close_style(
        one_has_attr=run_has_attr(prev_run, attribute),
        two_has_attr=run_has_attr(run, attribute),
        one_contains_break=run_contains_break(prev_run),
        output=output,
        attribute=attribute,
    )


def join_run_tags(run, prev_run, output=""):
    "process all the possible tags in the run"
    style_order = ["italic", "bold", "subscript", "superscript"]
    if run_has_attr(prev_run, "bold"):
        # close bold tags first if previous run was bold
        style_order = ["bold", "italic", "subscript", "superscript"]
    for style in style_order:
        output = run_open_close_style(run, prev_run, output, style)
    return output


def remove_odd_characters(string):
    """replace invisible whitespace characters"""
    # LINE SEPARATOR
    return string.replace(LINE_SEPARATOR, "")


def join_runs(runs):
    output = ""
    prev_run = None
    for run in runs:
        cleaned_text = remove_odd_characters(run.text)
        if cleaned_text.strip():
            output = join_run_tags(run, prev_run, output)
            output += cleaned_text
            prev_run = run
        else:
            # if the text is only whitespace then do not enclose it in tags
            output += cleaned_text
    # finish up by running one last time with prev_run
    output = join_run_tags("", prev_run, output)
    return output


if __name__ == "__main__":
    # debug while developing
    if len(sys.argv) != 2:
        sys.exit(
            "Usage: python {0} DOCX_FILE\nExample: python {0} 'tests/test_data/DIGEST 99999.docx'".format(
                *sys.argv
            )
        )

    DIGEST_CONTENT = parse_content(sys.argv[1])
    print(DIGEST_CONTENT.encode("utf-8"))

    """
    for file_name in ['DIGEST 20713.docx', 'DIGEST 24728.docx',
    'DIGEST 25783.docx', 'DIGEST 26726.docx']:
        print("\n\n")
        print(file_name)
        digest_content = parse_content(file_name)
        print(digest_content.encode('utf-8'))
    """
