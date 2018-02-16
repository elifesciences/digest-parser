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


def open_close_style(run, prev_run, output, attr='italic'):
    open_tag = None
    close_tag = None
    if attr == 'italic':
        open_tag = '<i>'
        close_tag = '</i>'
    if attr == 'bold':
        open_tag = '<b>'
        close_tag = '</b>'
    if not open_tag or not close_tag:
        return output
    # continue
    run_contains_break = bool(run.text.endswith("\n"))
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
        (getattr(run, attr) is True and (prev_run is None or getattr(prev_run, attr) is not True))
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
    content = parse_content('tests/test_data/DIGEST 99999.docx')
    print(content.encode('utf-8'))
