# cache4py: Caching simplified.

[![PyPI version shields.io](https://img.shields.io/pypi/v/cache4py.svg)](https://pypi.python.org/pypi/cache4py/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/cache4py.svg)](https://pypi.python.org/pypi/cache4py/)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)

## Getting started

### Installation
Install using pip: `$ pip install cache4py`

### Usage
```python
from cache4py.decorators import cache
from cache4py.storage.redis import RedisBackend

# You can choose memcached, redis or default (python's dict) as a backend.
redis_backend = RedisBackend(url='localhost', port='6379')

@cache(backend=redis_backend)
def my_function_one(*args, **kwargs):
    # do something awesome
    return
```

### Options
1. Keys
2. Eviction policies (coming soon)
3. Backend
4. Max memory limit (coming soon)
5. Key expiry time (coming soon)



## Contributing to cache4py

Refer CONTRIBUTING.md

## Issue tracking

Create issues at [cache4py/issues](https://github.com/nitinl/cache4py/issues).

## Authors

* **Nitin Labhishetty ([lnitin94@gmail.com](mailto:lnitin94@gmail.com))**
* **Vaibhav Tulsyan ([vstulsyan@gmail.com](mailto:vstulsyan@gmail.com))**
