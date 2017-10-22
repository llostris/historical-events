import os

import pickle


def load_pickle(filename):
    if os.path.isfile(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)
    else:
        return {}


def save_pickle(data, filename):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)
