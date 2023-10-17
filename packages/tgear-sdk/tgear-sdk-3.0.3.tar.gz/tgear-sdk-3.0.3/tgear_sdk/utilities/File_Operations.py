import os

def create_dir(path):
    """
    Create directories if doesn't exists
    :param path: path of the directory
    :return: None
    """
    if not os.path.exists(path):
        os.makedirs(path)
        print("directory created")
    else:
        print("directory already exists")