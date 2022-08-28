import os
import contextlib
import uuid

from knack.util import CLIError

def sequence():
    x = 0
    while True:
        x += 1
        yield x

@contextlib.contextmanager
def push_directory(new_directory):
    previous_directory = os.getcwd()
    os.chdir(new_directory)
    try:
        yield
    finally:
        os.chdir(previous_directory)

def uid_for_path(path):
    return uuid.uuid5(uuid.NAMESPACE_DNS, path).hex

def media_type_for_filename(filename):
    suffix = filename.suffix
    if (suffix=='.css'):
        return 'text/css'
    elif (suffix=='.ttf'):
        return 'application/vnd.ms-opentype'
    elif (suffix=='.ttc'):
        return 'application/vnd.ms-opentype'
    elif (suffix=='.svg'):
        return 'image/svg+xml'
    elif (suffix=='.png'):
        return 'image/png'
    elif (suffix=='.jpg'):
        return 'image/jpeg'
    elif (suffix=='.jpeg'):
        return 'image/jpeg'
    elif (suffix=='.gif'):
        return 'image/gif'
    elif (suffix=='.tiff'):
        return 'image/tiff'
    elif (suffix=='.tif'):
        return 'image/tiff'
    else:
        raise CLIError(f'Cannot resolve media type for: {filename.absolute()}')
