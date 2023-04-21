import pytest
from lru_cache import LRUCache
import tests.func_set1
import tests.func_set2


@pytest.fixture(autouse=True)
def reset_cache():
    LRUCache.reset()

def test_max_storage_sizes():
    with pytest.raises(AssertionError):
        @LRUCache(-1)
        def func():
            pass

        res = func()

    assert LRUCache._LRUCache__max_storage_size == 2
    assert len(LRUCache._LRUCache__keys_queue) == 0
    assert len(LRUCache._LRUCache__storage) == 0

    with pytest.raises(AssertionError):
        @LRUCache(0)
        def func():
            pass

        res = func()

    @LRUCache(1)
    def func():
        pass

    res = func()

def test_no_arguments_cached_call():
    @LRUCache(2)
    def no_args_fn():
        return 12345

    assert LRUCache._LRUCache__max_storage_size == 2
    assert len(LRUCache._LRUCache__keys_queue) == 0
    assert len(LRUCache._LRUCache__storage) == 0

    res = no_args_fn()
    assert LRUCache._LRUCache__max_storage_size == 2
    assert len(LRUCache._LRUCache__keys_queue) == 1
    assert len(LRUCache._LRUCache__storage) == 1

    res = no_args_fn()
    assert LRUCache._LRUCache__max_storage_size == 2
    assert len(LRUCache._LRUCache__keys_queue) == 1
    assert len(LRUCache._LRUCache__storage) == 1


def test_single_argument_cached_call():
    @LRUCache(2)
    def single_arg_fn(arg):
        return arg

    assert len(LRUCache._LRUCache__keys_queue) == 0
    assert len(LRUCache._LRUCache__storage) == 0

    res = single_arg_fn(1)
    assert len(LRUCache._LRUCache__keys_queue) == 1
    assert len(LRUCache._LRUCache__storage) == 1

    res = single_arg_fn(2)
    assert len(LRUCache._LRUCache__keys_queue) == 2
    assert len(LRUCache._LRUCache__storage) == 2

    res = single_arg_fn(2)
    assert len(LRUCache._LRUCache__keys_queue) == 2
    assert len(LRUCache._LRUCache__storage) == 2

    next_new_key = LRUCache._LRUCache__keys_queue[1]
    res = single_arg_fn(3)
    assert len(LRUCache._LRUCache__keys_queue) == 2
    assert len(LRUCache._LRUCache__storage) == 2
    assert next_new_key == LRUCache._LRUCache__keys_queue[0]

def test_two_named_args():
    @LRUCache(2)
    def two_named_args_fn(**kwargs):
        return '|'.join(kwargs)

    assert len(LRUCache._LRUCache__keys_queue) == len(LRUCache._LRUCache__storage) == 0

    two_named_args_fn(a=1, b=2)

    assert len(LRUCache._LRUCache__keys_queue) == len(LRUCache._LRUCache__storage) == 1

    two_named_args_fn(b=2, a=1)

    assert len(LRUCache._LRUCache__keys_queue) == len(LRUCache._LRUCache__storage) == 1

    two_named_args_fn(b=2, a=2)

    assert len(LRUCache._LRUCache__keys_queue) == len(LRUCache._LRUCache__storage) == 2

def test_same_func_name_diff_paths():
    assert len(LRUCache._LRUCache__keys_queue) == 0
    assert len(LRUCache._LRUCache__storage) == 0

    tests.func_set1.func_for_test('abc')

    assert len(LRUCache._LRUCache__keys_queue) == 1
    assert len(LRUCache._LRUCache__storage) == 1

    tests.func_set2.func_for_test('cba')

    assert len(LRUCache._LRUCache__keys_queue) == 2
    assert len(LRUCache._LRUCache__storage) == 2


def test_multiple_arguments_cached_call():
    @LRUCache(2)
    def multiple_args_fn(arg1, arg2, arg3=5):
        return arg1 + arg2 + arg3

    assert len(LRUCache._LRUCache__keys_queue) == 0
    assert len(LRUCache._LRUCache__storage) == 0

    res = multiple_args_fn(1, 2)
    assert len(LRUCache._LRUCache__keys_queue) == 1
    assert len(LRUCache._LRUCache__storage) == 1

    res = multiple_args_fn(2, 3)
    assert len(LRUCache._LRUCache__keys_queue) == 2
    assert len(LRUCache._LRUCache__storage) == 2

    res = multiple_args_fn(2, arg2=6)
    assert len(LRUCache._LRUCache__keys_queue) == 2
    assert len(LRUCache._LRUCache__storage) == 2

    next_new_key = LRUCache._LRUCache__keys_queue[1]
    res = multiple_args_fn(3, 9)
    assert len(LRUCache._LRUCache__keys_queue) == 2
    assert len(LRUCache._LRUCache__storage) == 2
    assert next_new_key == LRUCache._LRUCache__keys_queue[0]


