from parse import parse_content
from objects import Digest, Image


def build_digest(file_name, image_file_name=None):
    "build a digest object from a DOCX input file"
    digest = None
    content = parse_content(file_name)
    if content:
        digest = Digest()
        # todo - parse the content

    return digest
