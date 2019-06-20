from digestparser.parse import parse_content
from digestparser.objects import Digest, Image
from digestparser.zip import unzip_zip
from digestparser import LOGGER


SECTION_MAP = {
    'author': '<b>AUTHOR</b>',
    'title': '<b>DIGEST TITLE</b>',
    'summary': '<b>DIGEST ONE-SENTENCE SUMMARY</b>',
    'keywords': '<b>KEYWORDS</b>',
    'doi': '<b>FULL ARTICLE DOI</b>',
    'manuscript_number': '<b>MANUSCRIPT NUMBER</b>',
    'text': '<b>DIGEST TEXT</b>',
    'image': '<b>IMAGE CREDIT</b>',
}


def extract_section_content(section_name, content):
    "scan the content finding the content for the particular section"
    section_content = []
    target_section_heading = SECTION_MAP.get(section_name)
    extract_line = False
    for line in content.split("\n"):
        stripped_line = line.lstrip().rstrip()
        if stripped_line == target_section_heading:
            # content will start on the next line
            extract_line = True
            continue
        if extract_line:
            # read lines until a new section heading is encountered
            if stripped_line not in SECTION_MAP.values():
                section_content.append(stripped_line)
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


def build_author(content):
    author = build_singleton('author', content)
    return author.rstrip() if author else None


def build_title(content):
    return build_singleton('title', content)


def build_summary(content):
    return build_singleton('summary', content)


def build_keywords(content):
    raw_keywords = build_singleton('keywords', content)
    if raw_keywords:
        # split the comma separated keywords and strip whitespace
        return [key.lstrip().rstrip() for key in raw_keywords.split(',')]
    return raw_keywords


def build_manuscript_number(content):
    return build_singleton('manuscript_number', content)


def build_doi(content, digest_config):
    "prefer formatting the manuscript number into a doi, if not available use the doi from the docx"
    doi = None
    manuscript_number = build_manuscript_number(content)
    if manuscript_number and digest_config and digest_config.get('doi_pattern'):
        doi = digest_config.get('doi_pattern').format(msid=manuscript_number)
    else:
        # look for a doi
        doi = build_singleton('doi', content)
    return doi


def build_text(content):
    return build_list('text', content)


def build_image(content, image_file_name=None):
    image_content = build_singleton('image', content)
    if not image_content:
        return None
    image_object = Image()
    image_object.caption = image_content
    if image_file_name:
        image_object.file = image_file_name
    return image_object


def handle_zip(file_name, temp_dir):
    "if the file is a zip, extract, otherwise just a docx"
    docx_file_name = None
    image_file_name = None
    if file_name.endswith('.zip'):
        docx_file_name, image_file_name = unzip_zip(file_name, temp_dir)
    else:
        docx_file_name = file_name
    return docx_file_name, image_file_name


def build_digest(file_name, temp_dir='tmp', digest_config=None, image_file_name=None):
    "build a digest object from a DOCX input file"
    digest = None
    docx_file_name, zip_image_file_name = handle_zip(file_name, temp_dir)
    LOGGER.info(
        "build_digest file '%s' has docx_file_name: '%s'", file_name, docx_file_name)
    LOGGER.info(
        "build_digest file '%s' has zip_image_file_name: '%s'", file_name, zip_image_file_name)
    if not image_file_name:
        image_file_name = zip_image_file_name
    content = parse_content(docx_file_name)
    if content:
        digest = Digest()
        digest.author = build_author(content)
        digest.title = build_title(content)
        digest.summary = build_summary(content)
        digest.keywords = build_keywords(content)
        digest.manuscript_number = build_manuscript_number(content)
        digest.doi = build_doi(content, digest_config)
        digest.text = build_text(content)
        digest.image = build_image(content, image_file_name)
    return digest
