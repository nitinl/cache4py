# cache4py
Caching simplified.

## Getting started

### Installation
Install using pip: `$ pip install cache4py`

### Usage
```python
from cache4py import cache, LRU, Backend

# You can choose memcached, redis or default (python's dict) as a backend.
redis_backend = Backend(variant=Backend.REDIS, url='', port='')

@cache(eviction_policy=LRU, backend=redis_backend)
def my_function_one(*args, **kwargs):
    # do something awesome
    return
```

### Options
1. Keys
2. Eviction policies
3. Backend
4. Max memory limit
5. Key expiry time



## Contributing to cache4py

These instructions will get you a copy of the project up and running on your local machine for development and testing.
 TODO

### Prerequisites

Install the python package requirements using the following command:

```
pip install -r requirements.txt
```
### Running the tests

Run unit tests using the command: `TODO`

## Issue tracking

Create issues at [cache4pd/issues](https://github.com/nitinl/cache4py/issues).

## Authors

* **Nitin Labhishetty ([lnitin94@gmail.com](mailto:lnitin94@gmail.com))**
* **Vaibhav Tulsyan ([vstulsyan@gmail.com](mailto:vstulsyan@gmail.com))**
