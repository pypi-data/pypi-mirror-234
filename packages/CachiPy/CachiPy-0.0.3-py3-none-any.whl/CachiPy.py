import functools
from collections import OrderedDict

def cacheit(func):
    cache = OrderedDict()
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = (func.__name__, args, frozenset(kwargs.items()))
        
        if key in cache:return cache[key]
        
        result = func(*args, **kwargs);cache[key] = result;return result
    
    def clear_cache():
        nonlocal cache
        cache = {}
    
    wrapper.clear_cache = clear_cache
    return wrapper