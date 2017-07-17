"""
Author: nitin
Date: 18/7/17
Description: 
"""
from decorators import cache
from backends import RedisBackend
import time
from math import factorial

from utils import args_to_key, hash_key

redis_backend = RedisBackend('localhost', 6379)


@cache(backend=redis_backend)
def redis_target_function(x):
    return factorial(x)

def uncached_target_function(x):
    return factorial(x)

def test_redis():
    print("Start test")
    start_time = time.time()
    for i in range(5):
      result = uncached_target_function(75000)
    first_elapsed_time = time.time() - start_time
    start_time = time.time()
    for i in range(5):
      result = redis_target_function(75000)
    second_elapsed_time = time.time() - start_time
    print("Time difference: before: {0}, after: {1}".format(first_elapsed_time, second_elapsed_time))
    hashed_key = hash_key(75000)
    redis_backend.delete(key_name=hashed_key)

if __name__ == '__main__':
    print('aaya')
    test_redis()
