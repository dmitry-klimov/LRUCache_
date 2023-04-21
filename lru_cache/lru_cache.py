class LRUCache(object):
    """
    Decided to use dedicated List to keep working with __storage as simple and fast as it could be.
    We still can use something like {(key, key_index): value}, but it will increase complexity upto O(n)
    """
    __storage = {}
    __keys_queue = []
    __max_storage_size = None

    def __init__(self, max_storage_size):
        assert max_storage_size > 0
        self.__class__.__max_storage_size = max_storage_size

    @classmethod
    def get(cls, key):
        return cls.__storage[key]

    @classmethod
    def put(cls, key, data):
        if len(cls.__storage.keys()) >= cls.__max_storage_size:
            cls.__delete_first_record()
        cls.__storage[key] = data
        cls.__keys_queue.append(key)

    @classmethod
    def reset(cls):
        cls.__storage = {}
        cls.__keys_queue = []

    @classmethod
    def __delete_first_record(cls):
        del cls.__storage[cls.__keys_queue.pop(0)]
    @staticmethod
    def _get_key(func, args, kwargs):
        return f'{func}_{LRUCache.__get_args_hash(args)}_{LRUCache.__get_kwargs_hash(kwargs)}'

    def __call__(self, func):
        def _wrapper(*args, **kwargs):
            key = self.__class__._get_key(func, args, kwargs)
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
            # TODO Check built-in "hash()" function to minimize super-long strings impact
            parts.append(f'{i}_{val.__class__}_{val}')
        return '__'.join(parts)

    @staticmethod
    def __get_kwargs_hash(kwargs):
        parts = []
        for key in sorted(kwargs.keys()):
            # kwarg hash format: argName_argClass_argVal
            # TODO Check built-in "hash()" function to minimize super-long strings impact
            value = kwargs[key]
            parts.append(f'{key}_{value.__class__}_{value}')
        return '_'.join(parts)
