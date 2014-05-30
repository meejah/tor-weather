"""
Cache Implementation for the wrapper
"""

import json

ONIONOO_PARAMS = [
    'type',
    'running',
    'search',
    'lookup',
    'country',
    'as',
    'flag',
    'first_seen_days',
    'last_seen_says',
    'contact',
    'fields',
    'order',
    'offset',
    'limit'
]


def key_serializer(query, params):
    s = query + ';'
    for key in ONIONOO_PARAMS:
        s = s + str(params.get(key))+';'
    return s


def json_serializer(key, value):
    if type(value) == str:
        return value, 1
    return json.dumps(value).encode('utf-8'), 2


def json_deserializer(key, value, flags):
    if flags == 1:
        return value
    if flags == 2:
        return json.loads(value.decode('utf-8'))
    raise Exception("Unknown serialization format")


class SimpleCache():
    def __init__(self):
        self.dict = {}

    def get(self, query, params):
        return self.dict.get(key_serializer(query, params))

    def set(self, query, params, document):
        self.dict[key_serializer(query, params)] = document


class Memcache():
    def __init__(self, host=('localhost', 11211)):
        from pymemcache.client import Client
        self.memcached_client = Client(self.memcached_host,
                                       serializer=json_serializer,
                                       deserializer=json_deserializer)

    def get(self, query, params):
        return self.memcached_client.get(key_serializer(query, params))

    def set(self, query, params, document):
        return self.memcache_client.set(key_serializer(query, params),
                                        document)
