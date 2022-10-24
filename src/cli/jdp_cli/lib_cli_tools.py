import os
import contextlib

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
        