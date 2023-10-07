import json

from .config import get_store_reader


def get_cache_filename():
    return f".{get_store_reader()('ENV')}-cache.json"


def cache_read():
    try:
        with open(get_cache_filename(), 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}


def cache_write(cache):
    with open(get_cache_filename(), 'w') as f:
        json.dump(cache, f, indent=2)


def cache_set(key):
    def with_value(value):
        cache = cache_read()
        cache[key] = value
        cache_write(cache)
        return value
    return with_value


def cache_get(key):
    cache = cache_read()
    return cache.get(key)


def retrieve_and_cache(key=None, arg=None, describe_func=None):
    
    def with_func(func):
        resp = cache_get(key)
        if resp is None:
            print(f"Cache miss key <{key}>")
            if arg is None:
                retrieve_result = func()
            else:
                retrieve_result = func(arg)
            cache_set(key)(retrieve_result)
        else:
            print(f"Cache hit key <{key}>")
        resp = cache_get(key)
        print(f"{key}: {describe_func(resp)}")
        return resp
    return with_func
