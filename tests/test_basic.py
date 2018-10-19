"""
Author: nitin
Date: 18/7/17
Description: 
"""
import time
from math import factorial

from cache4py.decorators import cache
from cache4py.storage.memcached import MemcachedBackend
from cache4py.storage.redis import RedisBackend
from cache4py.utils import hash_key

redis_backend = RedisBackend('localhost', 6379)
memcached_backend = MemcachedBackend('127.0.0.1', 11211)

@cache(backend=redis_backend)
def redis_target_function(x):
    return factorial(x)

@cache(backend=memcached_backend)
def memcached_target_function(x):
    return factorial(x)


def uncached_target_function(x):
    return factorial(x)


def test_redis():
    print("Start redis caching test")

    start_time = time.time()
    for i in range(5):
      _ = uncached_target_function(75000)
    uncached_time = time.time() - start_time

    start_time = time.time()
    for i in range(5):
      _ = redis_target_function(75000)
    cached_time = time.time() - start_time

    print("Time difference: before: {0}, after: {1}".format(uncached_time, cached_time))

    assert(cached_time < uncached_time)

    hashed_key = hash_key(75000)
    redis_backend.delete(key_name=hashed_key)

def test_memcached():
    print("Start memcached caching test")

    start_time = time.time()
    for i in range(5):
      _ = uncached_target_function(75000)
    uncached_time = time.time() - start_time

    start_time = time.time()
    for i in range(5):
      _ = memcached_target_function(75000)
    cached_time = time.time() - start_time

    print("Time difference: before: {0}, after: {1}".format(uncached_time, cached_time))

    assert(cached_time < uncached_time)

    hashed_key = hash_key(75000)
    memcached_backend.delete(key_name=hashed_key)
