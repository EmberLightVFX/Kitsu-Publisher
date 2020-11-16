import copy
import datetime
import json

from functools import wraps

cache_settings = {"enabled": False}
cached_functions = []


def enable():
***REMOVED***
    Enable caching on all decorated functions.
***REMOVED***
    cache_settings["enabled"] = True
    return cache_settings["enabled"]


def disable():
***REMOVED***
    Disable caching on all decorated functions.
***REMOVED***
    cache_settings["enabled"] = False
    return cache_settings["enabled"]


def clear_all():
***REMOVED***
    Clear all cached functions.
***REMOVED***
    for function in cached_functions:
        function.clear_cache()


def remove_oldest_entry(memo, maxsize):
***REMOVED***
    Remove the oldest cache entry if there is more value stored than allowed.

    Params:
        memo (dict): Cache used for function memoization.
        maxsize (int): Maximum number of entries for the cache.

    Returns:
        Oldest entry for given cache.
***REMOVED***
    oldest_entry = None
    if maxsize > 0 and len(memo) > maxsize:
        oldest_entry_key = list(memo.keys())[0]
        for entry_key in memo.keys():
            oldest_date = memo[oldest_entry_key]["date_accessed"]
            if memo[entry_key]["date_accessed"] < oldest_date:
                oldest_entry_key = entry_key
        memo.pop(oldest_entry_key)
    return oldest_entry


def get_cache_key(args, kwargs):
***REMOVED***
    Serialize arguments to get a cache key. It will be used to store function
***REMOVED***s.

    Returns:
        str: generated key
***REMOVED***
    if len(args) == 0 and len(kwargs) == 0:
        return ""
    elif len(args) == 0:
        return json.dumps(kwargs)
    elif len(kwargs.keys()) == 0:
        return json.dumps(args)
***REMOVED***
        return json.dumps([args, kwargs])


def insert_value(function, cache_store, args, kwargs):
***REMOVED***
    Serialize function call arguments and store function result in given cache
    store.

    Args:
        function (func): The function to cache value for.
        cache_store (dict): The cache which will contain the value to cache.
        args, kwargs: The arguments for which a cache must be set.

    Returns:
        The cached value.
***REMOVED***
    returned_value = function(*args, **kwargs)
    key = get_cache_key(args, kwargs)
    cache_store[key] = {
        "date_accessed": datetime.datetime.now(),
        "value": returned_value,
    }
    return get_value(cache_store, key)


def get_value(cache_store, key):
***REMOVED***
    It generates a deep copy of the requested value. It's needed because if a
    pointer is returned, the value can be changed. Which leads to a modified
    cache and unexpected results.

    Returns:
        Value matching given key inside given cache store
***REMOVED***
    value = cache_store[key]["value"]
    return copy.deepcopy(value)


def is_cache_enabled(state):
***REMOVED***
    Args:
        state: The state describing the cache state.

    Returns:
        True if cache is enabled for given state.
***REMOVED***
    return cache_settings["enabled"] and state["enabled"]


def is_cache_expired(memo, state, key):
***REMOVED***
    Check if cache is expired (outdated) for given wrapper state and cache key.

    Args:
        memo (dict): The function cache
        state (dict): The parameters of the cache (enabled, expire, maxsize)
        key: The key to check

    Returns:
        True if cache value is expired.

***REMOVED***
    date = memo[key]["date_accessed"]
    expire = state["expire"]
    date_to_check = date + datetime.timedelta(seconds=expire)
    return expire > 0 and date_to_check < datetime.datetime.now()


def cache(function, maxsize=300, expire=120):
***REMOVED***
    Decorator that generate cache wrapper and that adds cache feature to
    target function. A max cache size and and expiration time (in seconds) can
    be set too.

    Args:
        function (func): Decorated function:
        maxsize: Number of value stored in cache (300 by default).
        expire: Time to live in seconds of stored value (disabled by default)
***REMOVED***
    cache_store = {}
    state = {"enabled": True, "expire": expire, "maxsize": maxsize}

    statistics = {
        "hits": 0,
        "misses": 0,
        "expired_hits": 0
    }

    def clear_cache():
        cache_store.clear()

    def get_cache_infos():
        size = {'current_size': len(cache_store)}
        infos = {}
        for d in [state, statistics, size]:
            infos.update(d)

        return infos

    def set_expire(new_expire):
        state["expire"] = new_expire

    def set_max_size(maxsize):
        state["maxsize"] = maxsize

    def enable_cache():
        state["enabled"] = True

    def disable_cache():
        state["enabled"] = False

    @wraps(function)
    def wrapper(*args, **kwargs):

        if is_cache_enabled(state):
            key = get_cache_key(args, kwargs)

            if key in cache_store:
                if is_cache_expired(cache_store, state, key):
                    statistics["expired_hits"] += 1
        ***REMOVED*** insert_value(function, cache_store, args, kwargs)
        ***REMOVED***
                    statistics["hits"] += 1
        ***REMOVED*** get_value(cache_store, key)

    ***REMOVED***
                statistics["misses"] += 1
    ***REMOVED***ed_value = insert_value(
                    function, cache_store, args, kwargs
        ***REMOVED***
                remove_oldest_entry(cache_store, state["maxsize"])
    ***REMOVED*** returned_value

***REMOVED***
***REMOVED*** function(*args, **kwargs)

    wrapper.set_cache_expire = set_expire
    wrapper.set_cache_max_size = set_max_size
    wrapper.clear_cache = clear_cache
    wrapper.enable_cache = enable_cache
    wrapper.disable_cache = disable_cache
    wrapper.get_cache_infos = get_cache_infos

    cached_functions.append(wrapper)
    return wrapper
