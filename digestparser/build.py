from digestparser.parse import parse_content
from digestparser.objects import Digest, Image

SECTION_MAP = {
    'title': '<b>DIGEST TITLE</b>',
    'summary': '<b>DIGEST ONE-SENTENCE SUMMARY</b>',
    'keywords': '<b>KEYWORDS</b>',
    'doi': '<b>FULL ARTICLE DOI</b>',
    'text': '<b>DIGEST TEXT</b>',
    'image': '<b>IMAGE CREDIT</b>',
}

def extract_section_content(section_name, content):
    "scan the content finding the content for the particular section"
    section_content = []
    target_section_heading = SECTION_MAP.get(section_name)
    extract_line = False
    for line in content.split("\n"):
        if line == target_section_heading:
            # content will start on the next line
            extract_line = True
            continue
        if extract_line:
            # read lines until a new section heading is encountered
            if line not in SECTION_MAP.values():
                section_content.append(line)
            else:
                break
    return section_content

def build_singleton(section_name, content):
    "extract the content section and return a single value"
    section_content = extract_section_content(section_name, content)
    if not section_content:
        return None
    return section_content[0]

def build_list(section_name, content):
    "extract the content and return a list of values"
    return extract_section_content(section_name, content)

def build_title(content):
    return build_singleton('title', content)

def build_summary(content):
    return build_singleton('summary', content)

def build_keywords(content):
    keywords = []
    raw_keywords = build_singleton('keywords', content)
    if raw_keywords:
        # split the comma separated keywords and strip whitespace
        return [key.lstrip().rstrip() for key in raw_keywords.split(',')]
    else:
        return raw_keywords

def build_doi(content):
    return build_singleton('doi', content)

def build_text(content):
    return build_list('text', content)

def extract_image_content(content):
    caption = None
    credit = None
    license_value = None
    # split the content into separate values
    first_parts = content.split('Image credit:')
    caption = first_parts[0].rstrip()
    # continue to split up the final parts
    second_parts = first_parts[1].split('(')
    credit = second_parts[0].lstrip().rstrip()
    license_value = second_parts[1].rstrip(' )')
    return caption, credit, license_value

def build_image(content):
    image_content = build_singleton('image', content)
    if not image_content:
        return None
    image_object = Image()
    # extract the content parts
    caption, credit, license_value = extract_image_content(image_content)
    image_object.caption = caption
    image_object.credit = credit
    image_object.license = license_value
    return image_object


def build_digest(file_name, image_file_name=None):
    "build a digest object from a DOCX input file"
    digest = None
    content = parse_content(file_name)
    if content:
        digest = Digest()
        digest.title = build_title(content)
        digest.summary = build_summary(content)
        digest.keywords = build_keywords(content)
        digest.doi = build_doi(content)
        digest.text = build_text(content)
        digest.image = build_image(content)
    return digest
