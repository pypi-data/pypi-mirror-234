import re

def is_valid_classifier(classifier):
    return bool(re.match("^[a-zA-Z0-9_-]+$", classifier))