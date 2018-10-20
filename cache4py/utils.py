"""
Author: nitin
Date: 18/7/17
Description: 
"""

import pickle
from hashlib import sha224


def args_to_key(*args, **kwargs):
    """
    Makes a single object from given args and kwargs.
    :param args: Args list.
    :param kwargs: Kwargs dictionary.
    :return: A combined object of the given args and kwargs.
    """
    params = args
    if kwargs:
        # sort dictionary keys and merge to match inputs where user changes order of kwargs.
        _kwmark = (object(),)
        params += sum(sorted(kwargs.items()), _kwmark)
    return params


def hash_key(python_object):
    """
    Computes a consistent sha224 hash for given object.
    :param python_object: A python object.
    :return: Consistent sha224 hash for the key_object.
    """
    serialized_key = pickle.dumps(python_object, protocol=pickle.HIGHEST_PROTOCOL)
    hashed_key = sha224(serialized_key).hexdigest()
    return hashed_key
