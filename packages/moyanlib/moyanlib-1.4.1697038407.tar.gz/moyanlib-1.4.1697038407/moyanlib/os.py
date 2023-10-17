import os
import moyanlib.Error as Error


def listdir(path):
    try:
        object = os.listdir(path)
    except:
        raise Error.file_PathError(path)
    else:
        return object


def create_dir(path):
    os.makedirs(path, exist_ok=True)


def remove_file(path):
    if os.path.exists(path):
        os.remove(path)


def move_file(src, dst):
    if os.path.exists(src):
        os.rename(src, dst)


def system(command):
    object = os.popen(command)
    text = object.read()
    return text
