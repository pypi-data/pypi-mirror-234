# encoding: utf-8
"""
@project: djangoModel->api_interrupter_wrapper
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 接口阻断器
@created_time: 2023/7/3 14:53
"""
from django.core.handlers.asgi import ASGIRequest
from django.core.handlers.wsgi import WSGIRequest
from rest_framework.request import Request


def api_interrupter_wrapper(func):
    """
    API阻断器，用于用户角色的权限判断装饰器，由
    """

    def wrapper(instance, arg_request=None, *args, request=None, request_params=None, user_info: dict = None, **kwargs):
        """
        @param instance 实例是一个APIView的实例
        @param request APIView实例会传入请求包
        @param request APIView实例会传入请求包
        :param user_info: token解析出的用户信息
        :param request_params: 请求参数
        """
        # =========== section 解析系统request对象 start ==================
        if isinstance(instance, WSGIRequest) or isinstance(instance, Request) or isinstance(instance, ASGIRequest):
            request = instance
        if isinstance(arg_request, WSGIRequest) or isinstance(arg_request, Request) or isinstance(arg_request, ASGIRequest):
            request = arg_request
        if request is None:
            return func(instance, request, *args, request=request, request_params=request_params, user_info=user_info, **kwargs, )
        # =========== section 解析系统request对象 end   ==================

        print("request, request_params, user_info:", request, request_params, user_info)

        result = func(instance, *args, request=request, request_params=request_params, user_info=user_info, **kwargs)
        return result

    return wrapper
