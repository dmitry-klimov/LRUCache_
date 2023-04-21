from lru_cache import LRUCache


@LRUCache(2)
def func_for_test(a):
    return f'{__file__}_{a}'