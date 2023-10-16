import re

def is_valid_filename(filename):
    return bool(re.match("^[a-zA-Z0-9_-]+$", filename))