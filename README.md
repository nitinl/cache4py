# cache4py
Caching simplified.

## Getting started

### Installation
Install using pip: `$ pip install cache4py`

### Usage
```python
from cache4py.decorators import cache
from cache4py.storage.backends import RedisBackend

# You can choose memcached, redis or default (python's dict) as a backend.
redis_backend = RedisBackend(url='localhost', port='6379')

@cache(backend=redis_backend)
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

Run unit tests using the command: 

```
pytest --cov=cache4py --cov-report html tests/
```

## Issue tracking

Create issues at [cache4py/issues](https://github.com/nitinl/cache4py/issues).

## Authors

* **Nitin Labhishetty ([lnitin94@gmail.com](mailto:lnitin94@gmail.com))**
* **Vaibhav Tulsyan ([vstulsyan@gmail.com](mailto:vstulsyan@gmail.com))**
