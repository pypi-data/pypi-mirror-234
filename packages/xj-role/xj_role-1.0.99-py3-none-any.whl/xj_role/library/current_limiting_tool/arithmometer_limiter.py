# encoding: utf-8
"""
@project: djangoModel->arithmometer_limiter
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 计数器限流器
@created_time: 2023/7/30 16:59
"""
import time


class ArithmometerLimiter():
    """
    计数限流器，好处简单，但是请求处理不平滑。
    """
    request_count = 0  # 请求次数
    limit_count = 100  # 限流次数
    interval = 1000  # 窗口时长
    current_timestamp = time.time()  # 当前是时间戳

    def __init__(self):
        self.request_count = 0  # 请求次数
        self.limit_count = 100  # 限流次数
        self.interval = 1000  # 窗口时长
        self.current_timestamp = time.time()  # 当前是时间戳

    def limit(self):
        """
        基础限流器
        :return: true:限流; false:不限流;
        """
        now = time.time()
        if now < self.current_timestamp + self.interval:  # 如果改在限流区间内
            if self.request_count + 1 > self.interval:
                return True
            self.request_count += 1
            return False
        else:  # 超出了限流区间，开启显得限流窗口
            self.current_timestamp = now
            self.limit_count = 1
            return False

    def distributed_limit(self):
        """
        分布式限流器，使用redis实现分布式限流
        :return: true:限流; false:不限流;
        """
        pass

    def user_limit(self):
        """
        用户限流器，限制单个用户的访问频率，超出访问频率，则限制IP访问。
        :return: true:限流; false:不限流;
        """
        pass
