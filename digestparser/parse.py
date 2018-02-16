from docx import Document

def parse_content(file_name):
    "return all the content for testing"
    content = ''
    document = Document(file_name)
    #print(document.core_properties.author)
    #print(document.paragraphs)
    for para in document.paragraphs:
        content += join_runs(para.runs) + "\n"
    return content

def html_open_tag(style):
    "for the style return the HTML open tag"
    style_map = {
        'italic': '<i>',
        'bold': '<b>'
    }
    return style_map.get(style)

def html_close_tag(style):
    "for the style return the HTML close tag"
    style_map = {
        'italic': '</i>',
        'bold': '</b>'
    }
    return style_map.get(style)

def html_open_close_tag(style):
    "return the HTML open and close tags for the style"
    return html_open_tag(style), html_close_tag(style)


def open_close_style(run, prev_run, output, attr='italic'):
    open_tag, close_tag = html_open_close_tag(style=attr)
    if not open_tag or not close_tag:
        return output
    # continue
    prev_run_contains_break = bool(prev_run.text.endswith("\n") if prev_run is not None else False)
    # add the close tag first
    if (
            (prev_run_contains_break and getattr(prev_run, attr) is True) or
            (getattr(run, attr) is not True and prev_run and getattr(prev_run, attr) is True)
        ):
        # check for new line
        if output.endswith("\n"):
            output = output.rstrip("\n") + close_tag + "\n"
        else:
            output += close_tag
    # add the open tag
    if (
            (prev_run_contains_break and getattr(run, attr) is True) or
            (getattr(run, attr) is True and
             (prev_run is None or getattr(prev_run, attr) is not True))
        ):
        output += open_tag
    return output

def join_runs(runs):
    output = ''
    prev_run = None
    for run in runs:
        output = open_close_style(run, prev_run, output, 'italic')
        output = open_close_style(run, prev_run, output, 'bold')
        output += run.text
        prev_run = run
    return output

if __name__ == "__main__":
    "debug while developing"
    digest_content = parse_content('tests/test_data/DIGEST 99999.docx')
    print(digest_content.encode('utf-8'))
