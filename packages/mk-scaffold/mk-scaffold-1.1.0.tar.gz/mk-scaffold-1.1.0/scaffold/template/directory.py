import os

from ..constants import TEMPLATE_NAME


def find(path):
    """
    Search given path, then path/file.yml
    """
    for file in path, os.path.join(path, TEMPLATE_NAME):
        if os.path.exists(file) and not os.path.isdir(file):
            return file, os.path.dirname(file)
    return False, False
