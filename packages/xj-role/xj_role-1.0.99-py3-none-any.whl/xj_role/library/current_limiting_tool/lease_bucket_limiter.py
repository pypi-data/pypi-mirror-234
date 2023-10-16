# encoding: utf-8
"""
@project: djangoModel->lease_bucket_limiter
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 桶漏限流器
@created_time: 2023/8/7 9:35
"""
from threading import RLock
from time import time

__all__ = ("LeakyBucket",)


class LeakyBucket(object):

    def __init__(self, capacity, leak_rate, is_lock=False):
        """
        :param capacity:  The total tokens in the bucket.
        :param leak_rate:  The rate in tokens/second that the bucket leaks
        """
        self._capacity = float(capacity)
        self._used_tokens = 0
        self._leak_rate = float(leak_rate)
        self._last_time = time()
        self._lock = RLock() if is_lock else None

    def get_used_tokens(self):
        if self._lock:
            with self._lock:
                return self._get_used_tokens()
        else:
            return self._get_used_tokens()

    def _get_used_tokens(self):
        now = time()
        delta = self._leak_rate * (now - self._last_time)
        self._used_tokens = max(0, self._used_tokens - delta)
        return self._used_tokens

    def _consume(self, tokens):
        if tokens + self._get_used_tokens() <= self._capacity:
            self._used_tokens += tokens
            self._last_time = time()
            return True
        return False

    def consume(self, tokens):
        if self._lock:
            with self._lock:
                return self._consume(tokens)
        else:
            return self._consume(tokens)
