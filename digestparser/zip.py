import zipfile
import os
from digestparser.utils import sanitise


def profile_zip(file_name):
    "open the zip and get some file name data"
    zip_docx_file_name = None
    zip_image_file_name = None
    with zipfile.ZipFile(file_name, 'r') as open_zipfile:
        for zipfile_file in open_zipfile.namelist():
            # ignore files in subfolders like __MACOSX
            if '/' in zipfile_file:
                continue
            if zipfile_file.endswith('.docx'):
                zip_docx_file_name = zipfile_file
            else:
                # assume image file
                zip_image_file_name = zipfile_file
    return zip_docx_file_name, zip_image_file_name


def unzip_file(open_zipfile, zip_file_name, output_path):
    "read the zip_file_name from the open_zipfiel and write to output_path"
    with open_zipfile.open(zip_file_name) as zip_content:
        with open(output_path, 'wb') as output_file:
            output_file.write(zip_content.read())


def unzip_zip(file_name, temp_dir):
    "unzip certain files and return the local paths"
    docx_file_name = None
    image_file_name = None
    zip_docx_file_name, zip_image_file_name = profile_zip(file_name)
    # extract the files
    with zipfile.ZipFile(file_name, 'r') as open_zipfile:
        if zip_docx_file_name:
            docx_file_name = os.path.join(temp_dir, sanitise(zip_docx_file_name))
            unzip_file(open_zipfile, zip_docx_file_name, docx_file_name)
        if zip_image_file_name:
            image_file_name = os.path.join(temp_dir, sanitise(zip_image_file_name))
            unzip_file(open_zipfile, zip_image_file_name, image_file_name)
    return docx_file_name, image_file_name
