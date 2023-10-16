# encoding: utf-8
"""
@project: djangoModel->tool
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 最新版本的用户装饰器
@created_time: 2023/5/29 10:02
"""
from django.core.handlers.asgi import ASGIRequest
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from rest_framework.request import Request

from .custom_tool import dynamic_load_class


def parse_request_token(request=None):
    """解析用户token验证"""
    if not (isinstance(request, WSGIRequest) or isinstance(request, Request) or isinstance(request, ASGIRequest)):
        return {}, None
    token = request.headers.get('Authorization', None)
    UserService, import_err = dynamic_load_class(import_path="xj_user.services.user_service", class_name="UserService")
    if import_err:
        return {}, "该系统被没有安装用户模块"
    return UserService.check_token(token)


def user_authentication_wrapper(func):
    """
    用户认证装饰器，如果有Authorization则检查用户的有效性，如没有则认为用户以游客访问
    """

    def wrapper(instance, arg_request=None, *args, request=None, **kwargs):
        """
        @param instance 实例是一个APIView的实例
        @param request APIView实例会传入请求包
        @param request APIView实例会传入请求包
        @param args 其它可变参数元组
        @param kwargs 其它可变关键字参数字典
        """
        # =========== section 解析系统request对象 start ==================
        # print("> user_authentication_wrapper:", instance, request, args, kwargs)
        if isinstance(instance, WSGIRequest) or isinstance(instance, Request) or isinstance(instance, ASGIRequest):
            request = instance
        if isinstance(arg_request, WSGIRequest) or isinstance(arg_request, Request) or isinstance(arg_request, ASGIRequest):
            request = arg_request
        if request is None:
            return func(instance, request, *args, request=request, request_params={}, **kwargs, )
        # =========== section 解析系统request对象 end   ==================

        # =========== section 获取token并验证 start ==================
        token = request.headers.get('Authorization', None)
        # 如果没有传token则可视为以游客身份访问
        if not token or str(token) == 'null' or str(token).strip().upper() == "BEARER":
            return func(instance, request=request, user_info={}, *args, **kwargs)
        # 动态加载用户模块，进行权限验证
        UserService, import_err = dynamic_load_class(import_path="xj_user.services.user_service", class_name="UserService")
        if import_err:
            return JsonResponse({'err': 6001, 'msg': "该系统被没有安装用户模块"})
        user_serv, error_text = UserService.check_token(token)
        if error_text:
            return JsonResponse({'err': 6001, 'msg': error_text})
        # =========== section 获取token并验证 start ==================

        # =========== section 解析用户信息并返回 start ==================
        request.user = user_serv
        result = func(instance, *args, request=request, user_info=user_serv, **kwargs)
        return result
        # =========== section 解析用户信息并返回 end   ==================

    return wrapper


def user_authentication_force_wrapper(func):
    """
    用户认证装饰器，如果有Authorization则检查用户的有效性，如没有则认为用户以游客访问
    """

    def wrapper(*args, **kwargs):
        """
        @param instance 实例是一个APIView的实例
        @param request APIView实例会传入请求包
        @param request APIView实例会传入请求包
        @param args 其它可变参数元组
        @param kwargs 其它可变关键字参数字典
        """
        # =========== section 解析系统request对象 start ==================
        # print("> user_authentication_wrapper:", instance, request, args, kwargs)
        request = None
        for ins in args:
            if isinstance(ins, WSGIRequest) or isinstance(ins, Request) or isinstance(ins, ASGIRequest):
                request = ins
        for ins_name, ins in kwargs.items():
            if isinstance(ins, WSGIRequest) or isinstance(ins, Request) or isinstance(ins, ASGIRequest):
                request = ins

        if request is None:
            return func(*args, **kwargs)
        # =========== section 解析系统request对象 end   ==================

        # =========== section 获取token并验证 start ==================
        token = request.headers.get('Authorization', None)
        # 没有token直接返回6000异常
        if not token or str(token) == 'null' or str(token).strip().upper() == "BEARER":
            return JsonResponse({'err': 6000, 'msg': '该用户未登录'})
        # 动态加载用户模块，进行权限验证
        UserService, import_err = dynamic_load_class(import_path="xj_user.services.user_service", class_name="UserService")
        if import_err:
            return JsonResponse({'err': 6001, 'msg': "该系统被没有安装用户模块"})
        user_serv, error_text = UserService.check_token(token)
        if error_text:
            return JsonResponse({'err': 6001, 'msg': error_text})
        # =========== section 获取token并验证 start ==================

        # =========== section 解析用户信息并返回 start ==================
        request.user = user_serv
        kwargs.pop("user_info", None)
        result = func(*args, user_info=user_serv, **kwargs)
        return result
        # =========== section 解析用户信息并返回 end   ==================

    return wrapper
