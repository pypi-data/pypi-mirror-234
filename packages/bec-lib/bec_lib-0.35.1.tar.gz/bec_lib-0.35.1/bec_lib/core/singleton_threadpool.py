from concurrent.futures import ThreadPoolExecutor


# pylint: disable=too-few-public-methods
class SingletonThreadpool:
    """Singleton class for handling threadpools: Instantiating a new class instance
    is idempotent and will return the already existing class. However, the number of
    workers can be increased by instantiating a new class instance.

    >>> pool = SingleThreadpool(max_workers=100)
    # number of max_workers of pool == 100
    >>> pool2 = SingletonThreadpool(max_workers=110)
    # number of max_workers pool and pool2 == 110
    """

    DEFAULT_MAX_WORKER = 100
    executor = None

    def __init__(self, max_workers=DEFAULT_MAX_WORKER) -> None:
        if self.executor is None:
            self.executor = ThreadPoolExecutor(max_workers=max_workers)
        if max_workers > self.executor._max_workers:
            self.executor._max_workers = max_workers

    def __new__(cls, max_workers=DEFAULT_MAX_WORKER):
        if not hasattr(cls, "_threadpool"):
            cls._threadpool = super(SingletonThreadpool, cls).__new__(cls)
        return cls._threadpool
