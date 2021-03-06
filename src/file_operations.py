import os

import pickle


def load_pickle(filename, is_dict=False, is_list=False, is_set=False):
    if os.path.isfile(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)
    else:
        if is_dict:
            return {}
        if is_list:
            return []
        if is_set:
            return set()


def save_pickle(data, filename):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)


def get_filepath(directory: str, filename: str, ext: str = None):
    if ext:
        return "{}/{}.{}".format(directory, filename, ext)
    else:
        return "{}/{}".format(directory, filename)


def build_path(parts: list):
    return '/'.join(parts)
