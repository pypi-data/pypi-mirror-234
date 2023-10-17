# endcoding = utf-8
"""
author : vex1023
email :  vex1023@qq.com
各类型的decorator
"""


import signal
import time
from typing import Callable
from concurrent.futures import ThreadPoolExecutor, Future, Executor
from multiprocessing.pool import ThreadPool
from multiprocessing import Lock
from functools import wraps
from vxutils import logger


__all__ = [
    "retry",
    "timeit",
    "singleton",
    "threads",
    "lazy_property",
    "timeout",
]


###################################
# 错误重试方法实现
# @retry(tries, CatchExceptions=(Exception,), delay=0.01, backoff=2)
###################################


def retry(tries, cache_exceptions=(Exception,), delay=0.1, backoff=2):
    """
    错误重试的修饰器
    :param tries: 重试次数
    :param cache_exceptions: 需要重试的exception列表
    :param delay: 重试前等待
    :param backoff: 重试n次后，需要等待delay * n * backoff
    :return:
    @retry(5,ValueError)
    def test():
        raise ValueError
    """
    if backoff <= 1:
        raise ValueError("backoff must be greater than 1")

    if tries < 0:
        raise ValueError("tries must be 0 or greater")

    if delay <= 0:
        raise ValueError("delay must be greater than 0")

    if not isinstance(cache_exceptions, (tuple, list)):
        cache_exceptions = (cache_exceptions,)
    else:
        cache_exceptions = [
            err_cls for err_cls in cache_exceptions if issubclass(err_cls, Exception)
        ]

    def deco_retry(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            mdelay = delay
            for i in range(1, tries):
                try:
                    return f(*args, **kwargs)
                except Exception as err:
                    logger.warning(cache_exceptions)
                    if not isinstance(err, cache_exceptions):
                        raise err from err

                    logger.error(
                        "function %s(%s, %s) try %s times error: %s\n",
                        f.__name__,
                        args,
                        kwargs,
                        i,
                        str(err),
                    )
                    logger.warning("Retrying in %.4f seconds...", mdelay)

                    time.sleep(mdelay)
                    mdelay *= backoff

            return f(*args, **kwargs)

        return f_retry

    return deco_retry


###################################
# 计算运行消耗时间
# @timeit
###################################


def timeit(func):
    """
    计算运行消耗时间
    @timeit
    def test():
        time.sleep(1)
    """
    from vxutils import logger

    def wapper(*args, **kwargs):
        _start = time.perf_counter()
        retval = func(*args, **kwargs)
        _end = time.perf_counter()
        logger.info("function %s() used : %f:.6fs", func.__name__, (_end - _start))
        return retval

    return wapper


###################################
# Singleton 实现
# @singleton
###################################


class singleton(object):
    """
    单例
    example::

        @singleton
        class YourClass(object):
            def __init__(self, *args, **kwargs):
                pass
    """

    def __init__(self, cls):
        self._instance = None
        self._cls = cls
        self._lock = Lock()

    def __call__(self, *args, **kwargs):
        if self._instance is None:
            with self._lock:
                if self._instance is None:
                    self._instance = self._cls(*args, **kwargs)
        return self._instance


###################################
# 异步多线程
# @thread(n,timeout=None)
###################################


def __error_callback(self, e: Exception):
    """发生错误后，处理"""
    logger.error("thread error: %s", e)
    raise e from e


class vxthreads:
    """多线程装饰器"""

    _executor = ThreadPoolExecutor(thread_name_prefix="vxthreads")

    def __init__(
        self, time_out=5, callback: Callable = None, error_callback: Callable = None
    ) -> None:
        self._timeout = time_out
        self._callback = callback
        self._error_callback = error_callback or __error_callback

    def __call__(self, func: Callable) -> Callable:
        def decorator(func):
            @wraps(func)
            def warpped(*args, **kwargs):
                return AsyncResult(
                    self._executor.submit(func, *args, **kwargs),
                    timeout,
                )

            return warpped

        return decorator

    @classmethod
    def set_executor(cls, executor: Executor) -> None:
        """设置执行器"""
        cls._executor = executor


class AsyncResult:
    """异步返回结果"""

    def __init__(
        self,
        future: Future,
        timeout_time: float = 5,
        callback: Callable = None,
    ):
        self._future = future
        self._future.add_done_callback(callback)
        self._timeout = timeout_time
        self._result = None

    def __getattr__(self, name):
        if self._result is None:
            self._result = self._future.get(self._timeout)
        return getattr(self._result, name)


def threads(n, timeout=5):
    """多线程装饰器
    @thread(n,timeout=None)
    def handler(*args, **kwargs):
        pass

    rets = map(handler , iterable)
    for ret in rets:
        print(ret.get())
    """

    def decorator(f):
        pool = ThreadPool(n)

        @wraps(f)
        def warpped(*args, **kwargs):
            return AsyncResult(
                pool.apply_async(func=f, args=args, kwds=kwargs), timeout
            )

        return warpped

    return decorator


###################################
# 限制超时时间
# @timeout(seconds, error_message='Function call timed out')
###################################


def timeout(seconds, error_message="Function call timed out"):
    """超时限制装饰器

    Arguments:
        seconds -- 超时秒数

    Keyword Arguments:
        error_message -- 超时返回信息 (default: {"Function call timed out"})
    """

    def decorated(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(
                f"{error_message} after {seconds} seconds,{signum},{frame}"
            )

        @wraps(func)
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wrapper

    return decorated


###################################
# 类似@property的功能，但只执行一次
# @lazy_property
###################################


class lazy_property(object):
    """类似@property的功能，但只执行一次"""

    def __init__(self, deferred):
        self._deferred = deferred
        self.__doc__ = deferred.__doc__

    def __get__(self, obj, cls):
        if obj is None:
            return self
        value = self._deferred(obj)
        setattr(obj, self._deferred.__name__, value)
        return value
