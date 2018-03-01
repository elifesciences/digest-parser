"helper functions for running tests"
import os


def read_file(file_name_plus_path):
    "read file content"
    with open(file_name_plus_path, 'rb') as open_file:
        return open_file.read()

def fixture_path(file_name):
    "path for a file in the fixtures directory"
    return os.path.join('tests', 'fixtures', file_name)

def read_fixture(file_name):
    "read a file from the fixtures directory"
    return read_file(fixture_path(file_name))

def test_data_path(file_name):
    "path for a file in the test_data directory"
    return os.path.join('tests', 'test_data', file_name)
