"""
Author: nitin
Date: 18/7/17
Description: 
"""
from functools import wraps

from cache4py.exceptions import BackendException
from cache4py.utils import args_to_key, hash_key
from cache4py.storage.redis import RedisBackend


def cache(backend=RedisBackend, keys=args_to_key):
    """
    Cache decorator. Backend can be a python dict, redis or memcached server.
    """

    def _decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if backend is None:
                backend_exception_message = 'Invalid input None provided for backend.'
                raise BackendException(backend_exception_message)

            key = keys(*args, **kwargs)
            hashed_key = hash_key(key)

            result = backend.get(hashed_key)

            if result is not None:
                # cache hit
                return result

            # cache miss
            function_result = func(*args, **kwargs)

            # store result in cache
            backend.set(hashed_key, function_result)
            return function_result

        return wrapper

    return _decorator

