# encoding: utf-8
"""
@project: djangoModel->api_interrupter
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: API阻断器
@created_time: 2023/7/5 10:30
"""
import re

from django.db.models import F

from xj_role.models import RoleApi, UserToRole, RolePermission
from xj_role.utils.custom_tool import format_params_handle


class APIInterrupter():
    """API接口阻断器"""
    open_api_map = {}

    def __init__(self):
        self._get_open_api()

    def _get_open_api(self):
        """
        获取系统所有API
        :return: data, err
        """
        if not self.open_api_map:
            open_apis = RoleApi.objects.filter(is_delete=0, is_using=1, is_open_api=1).values("route", "method")
            open_api_map = {}
            for i in open_apis:
                route = i["route"]
                method = i["method"]
                # 开放API
                if open_api_map.get(route):
                    open_api_map[route].append(method)
                    open_api_map[route] = list(set(open_api_map[route]))
                else:
                    open_api_map[route] = [method]
            self.open_api_map = open_api_map
        return self.open_api_map

    def api_switch(self, api_route, method, **kwargs):
        """
        开放接口, 则直接放行s
        :param method: 请求方法
        :param api_route:请求路由
        :return: data, err
        """
        self._get_open_api()
        for patt in self.open_api_map.keys():
            old_patt = patt
            patt = re.sub("{.*?}", "(.*?)", patt)
            patt = patt.replace("//", "/").replace("//", "/").replace("//", "/").replace("//", "/").replace("//", "/").replace("//", "/")
            patt = patt + "?" if patt[-1:] == "/" else patt
            # 正则匹配成功且该请求方法允许请求
            if re.search(patt, api_route) and method in self.open_api_map.get(old_patt):
                return True, None
        return None, None

    @staticmethod
    def api_filter_value(*args, user_id, api_route, method, request_params, **kwargs):
        """
        接口值过滤
        :param request_params: 解析出的请求参数
        :param method: 请求方式
        :param user_id: 用户ID
        :param api_route: 接口路由
        :return: data, err
        """
        # 获取用户绑定的角色
        user_role_ids = list(UserToRole.objects.filter(
            user_id=user_id, role__is_delete=0, role__is_using=1
        ).values("role_id"))
        user_role_ids = [i["role_id"] for i in user_role_ids]

        # ------------------- section API权限处理 ---------------------------
        api_permission_list = RolePermission.objects.annotate(route=F("api__route"), method=F("api__method")).filter(
            role_id__in=user_role_ids,
            api__method=method,
            type="API",
            role__is_delete=0,
            role__is_using=1,
            api__is_delete=0,
            api__is_using=1,
            api__is_open_api=0
        ).values(
            "route", "method",
            "filter_filed_list",
            "remove_filed_list",
            "default_value_dict",
            "allow_values_dict",
            "output_filter_filed_list",
            "output_remove_filed_list",
        )
        # 权限匹配
        for i in api_permission_list:
            patt = i["route"]
            patt = re.sub("{.*?}", "(.*?)", patt)
            patt = patt.replace("//", "/").replace("//", "/").replace("//", "/").replace("//", "/").replace("//", "/").replace("//", "/")
            patt = patt + "?" if patt[-1:] == "/" else patt

            if re.search(patt, api_route):  # 匹配到路由
                request_params = format_params_handle(
                    param_dict=request_params,
                    filter_filed_list=i["filter_filed_list"],
                    remove_filed_list=i["remove_filed_list"]
                )

                # 默认值赋值
                allow_values_dict = i.get("allow_values_dict", {})
                allow_values_dict = allow_values_dict if isinstance(allow_values_dict, dict) else {}
                for k, v in allow_values_dict:
                    request_params.setdefault(k, v)

                # 移除值
                pass
                break
            # ------------------- section API权限处理 ---------------------------

            # ------------------- section 数据权限权限处理 ---------------------------
            data_set_type_to_key = {
                "THREAD": "category_id",
                "FINANCE": "sand_box_id",
                "USER": "user_group_id",
            }
            data_permission_list = RolePermission.objects.annotate(route=F("api__route"), method=F("api__method")).filter(
                role_id__in=user_role_ids,
                type="DATA",
                role__is_delete=0,
                role__is_using=1,
            ).values("data_set_type", "data_set_id")
            for i in data_permission_list:
                key = data_set_type_to_key.get(i["data_set_type"], None)
                if not key:
                    continue
                request_params.setdefault(key, i["data_set_id"])
            # ------------------- section 数据权限权限处理 ---------------------------

            return request_params, None

        return request_params, "您没有权限访问该接口"
