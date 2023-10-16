# encoding: utf-8
"""
@project: djangoModel->omnipotence_wrapper
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 万能装饰器
@created_time: 2023/6/30 14:27
"""
from .custom_tool import *


class OmnipotenceWrapper:
    """万能装饰器分发类"""

    default_wrappers = [
        {"path": "xj_role.utils.user_wrapper", "function": "user_authentication_force_wrapper", "must_run": True},
        {"path": "xj_role.utils.custom_tool", "function": "request_params_wrapper", "must_run": True},
    ]
    custom_run_wrappers = []  # 用户需要走执行的自定以装饰器
    run_wrappers_instance = []  # 先执行默认的装饰器，然后在执行自定义的装饰器

    def __init__(self, run_wrappers=None):
        # 获取默认执行的装饰器
        run_wrappers, err = force_transform_type(variable=run_wrappers, var_type="list")
        if run_wrappers:
            self.run_wrappers = run_wrappers

    def get_wrappers(self):
        """
        获取所有需要执行的装饰器
        :return:
        """
        for wrapper_map in self.default_wrappers:
            wrapper_function, err = dynamic_load_function(import_path=wrapper_map["path"], function_name=wrapper_map["function"])
            if err:
                continue
            self.run_wrappers_instance.append(wrapper_function)
        return self.run_wrappers_instance

    def run_wrapper(self, out_run_wrapper, inner_run_wrapper):
        """
        执行装饰器方法
        :param out_run_wrapper: 外层装饰器
        :param inner_run_wrapper: 内层装饰器
        """

        def inner_run():
            @out_run_wrapper
            def wrapper(*args, **kwargs):
                return inner_run_wrapper(*args, **kwargs)
            return wrapper
        return inner_run

    def wrapper(self, wrapper_list=[], ):
        """
        万能Http接口装饰器
        :param params:
        :param wrapper_list: 用户期望调用的的装饰器
        """

        def wrapper(func):
            def decorator(*args, **kwargs):
                copy_func = func
                run_wrappers = self.get_wrappers() + wrapper_list + [copy_func]
                out_run_wrapper, inner_run_wrapper = run_wrappers[0:2]
                for run_wrapper in run_wrappers[1:]:
                    copy_func = self.run_wrapper(out_run_wrapper=out_run_wrapper, inner_run_wrapper=run_wrapper)
                    out_run_wrapper = copy_func
                return copy_func

            return decorator

        return wrapper


wrapper = OmnipotenceWrapper()
omnipotence_wrapper = wrapper.wrapper
