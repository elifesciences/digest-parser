# coding=utf-8

import zipfile
import os
from digestparser.utils import sanitise
from digestparser import LOGGER


def profile_zip(file_name):
    "open the zip and get file info based on the filename"
    zip_docx_info = None
    zip_image_info = None
    with zipfile.ZipFile(file_name, 'r') as open_zipfile:
        for zipfile_info in open_zipfile.infolist():
            # ignore files in subfolders like __MACOSX
            zipfile_file = zipfile_info.filename
            if '/' in zipfile_file:
                continue
            if zipfile_file.endswith('.docx'):
                zip_docx_info = zipfile_info
            else:
                # assume image file
                zip_image_info = zipfile_info
    return zip_docx_info, zip_image_info


def unzip_file(open_zipfile, zip_file_info, output_path):
    "read the zip_file_info from the open_zipfile and write to output_path"
    with open_zipfile.open(zip_file_info) as zip_content:
        with open(output_path, 'wb') as output_file:
            output_file.write(zip_content.read())


def zip_output_name(file_name, temp_dir):
    "a safe output path to unzip a file to"
    LOGGER.info(
        "zip_output_name file_name before decoding is '%s'", file_name)
    try:
        file_name = file_name.encode('cp437').decode('utf8')
    except UnicodeDecodeError:
        file_name = file_name
    LOGGER.info(
        "zip_output_name file_name after decoding is '%s'", file_name)
    safe_file_name = sanitise(file_name)
    LOGGER.info(
        "zip_output_name file_name '%s' to safe_file_name '%s'", file_name, safe_file_name)
    try:
        zip_path = os.path.join(temp_dir.encode('utf8'), safe_file_name)
    except (UnicodeDecodeError, TypeError):
        zip_path = os.path.join(temp_dir, safe_file_name)
    LOGGER.info(
        "zip_output_name zip_path '%s' from temp_dir '%s', safe_file_name '%s'",
        zip_path, temp_dir, safe_file_name)
    return zip_path


def unzip_zip(file_name, temp_dir):
    "unzip certain files and return the local paths"
    docx_file_name = None
    image_file_name = None
    zip_docx_info, zip_image_info = profile_zip(file_name)
    # extract the files
    with zipfile.ZipFile(file_name, 'r') as open_zipfile:
        if zip_docx_info:
            docx_file_name = zip_output_name(zip_docx_info.filename, temp_dir)
            unzip_file(open_zipfile, zip_docx_info, docx_file_name)
        if zip_image_info:
            image_file_name = zip_output_name(zip_image_info.filename, temp_dir)
            unzip_file(open_zipfile, zip_image_info, image_file_name)
    return docx_file_name, image_file_name
