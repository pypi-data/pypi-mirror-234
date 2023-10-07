import os

from dotenv import dotenv_values

from .memoize import create_memoizer


def config():
    environment_name = os.environ.get('ENV', 'dev')
    os.environ['ENV'] = environment_name
    values = {
        **dotenv_values(f".{environment_name}.env"),
        **os.environ
    }
    return values


memoize = create_memoizer(config)


def get_store_reader():
    store = memoize()

    def get_env(key):
        return store.get(key)

    return get_env


def get_store_writer():
    store = memoize()

    def get_env_key_writer(key):
        def set_env_key(value):
            store[key] = value

        return set_env_key

    return get_env_key_writer
