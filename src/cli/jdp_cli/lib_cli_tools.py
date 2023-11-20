import os
import contextlib
import uuid

def sequence():
    x = 0
    while True:
        x += 1
        yield x

def uid_for_path(path):
    return uuid.uuid5(uuid.NAMESPACE_DNS, path).hex

@contextlib.contextmanager
def push_directory(new_directory):
    previous_directory = os.getcwd()
    os.chdir(new_directory)
    try:
        yield
    finally:
        os.chdir(previous_directory)
        