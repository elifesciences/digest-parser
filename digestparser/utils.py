"utility helper functions"
import re

def sanitise(file_name):
    "replace unwanted characters in file name if present"
    if not file_name:
        return file_name
    file_name = file_name.replace('/\\', '')
    file_name = re.sub(r'\.+', '.', file_name)
    return file_name
