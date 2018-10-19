"""
Author: nitin
Date: 18/7/17
Description: 
"""


class Cache4PyException(Exception):
    pass


class BackendException(Cache4PyException):
    pass


class RedisBackendException(BackendException):
    pass


class MemcachedBackendException(BackendException):
    pass
