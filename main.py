class LRUCache(object):
    _storage = {}
    _max_data_size = None
    _record_counter = 0

    def __init__(self, max_data_size):
        self.__class__._max_data_size = max_data_size

    @classmethod
    def get(cls, key):
        return cls._storage[key]

    @classmethod
    def put(cls, key, data):
        if len(cls._storage.keys()) > cls._max_data_size:
            # TODO Implement deletion according to records order
            record_to_delete = min(cls._storage.keys())
            del cls._storage[record_to_delete]
        cls._storage[key] = data
        cls._record_counter += 1

    @staticmethod
    def _get_hash(func, args, kwargs):
        return f'{func}_{LRUCache.__get_args_hash(args)}_{LRUCache.__get_kwargs_hash(kwargs)}'

    def __call__(self, func):
        def _wrapper(*args, **kwargs):
            key = self.__class__._get_hash(func, args, kwargs)
            try:
                data = self.get(key)
            except KeyError:
                data = func(*args, **kwargs)
                self.__class__.put(key, data)
            return data
        return _wrapper

    @staticmethod
    def __get_args_hash(args):
        parts = []
        for i, val in enumerate(args):
            # arg hash format: argNo_argClass_argVal
            # TODO Check built-in "hash()" function to minimize long strings impact
            parts.append(f'{i}_{val.__class__}_{val}')
        return '__'.join(parts)

    @staticmethod
    def __get_kwargs_hash(kwargs):
        parts = []
        for i in sorted(kwargs.keys()):
            # kwarg hash format: argNo_argClass_argName_argVal
            # TODO Check built-in "hash()" function to minimize long strings impact
            arg = kwargs[i]
            parts.append(f'{arg.__class__}_{arg.__name__}_{i}')
        return '_'.join(parts)


@LRUCache(5)
def test_fn1(a):
    return a


@LRUCache(5)
def test_fn2(a=1):
    return a * 3


@LRUCache(5)
def test_fn3(a, b, c):
    return a + b + c


if __name__ == "__main__":
    res = test_fn1(5)
    res = test_fn1(3)
    res = test_fn2(3)
    res = test_fn1(5)
