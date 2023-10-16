# encoding: utf-8
"""
@project: djangoModel->role_apis_services
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 角色PAI服务
@created_time: 2023/6/15 11:10
"""
import re

from django.core.paginator import Paginator, EmptyPage
from django_redis import get_redis_connection

from ..library.get_system_apis import GetSystemApis
from ..models import RoleApi
from ..utils.custom_tool import force_transform_type, format_params_handle


class RoleApiServices():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.redis_conn = get_redis_connection()

    @staticmethod
    def get_apis(params: dict = None, only_first: int = None, pagination=True, **kwargs):
        page, err = force_transform_type(variable=params.pop("page", 1), var_type="int", default=1)
        size, err = force_transform_type(variable=params.pop("size", 20), var_type="int", default=20)
        pagination, err = force_transform_type(variable=pagination, var_type="bool", default=True)
        only_first, err = force_transform_type(variable=only_first, var_type="bool", default=False)
        # 排序字段
        sort = params.get("sort", "-id")
        sort = sort if sort in [
            "id", "-id", "-created_time", "created_time", "update_time", "-update_time", "module", "-module"
        ] else "-created_time"

        params = format_params_handle(
            param_dict=params,
            filter_filed_list=["route|str", "method|str", "module|str", "name|str", "is_using|int", "is_open_api|int", ],
            alias_dict={"route": "route__contains", "name": "name__contains"}
        )
        params.setdefault("is_using", 1)
        params["is_delete"] = 0

        # 构建ORM
        query_set = RoleApi.objects.filter(**params).order_by(sort).values()

        # 单条详情查询
        if only_first:
            return query_set.first(), None

        # 不分页查询
        count = query_set.count()
        if not pagination and count <= 500:
            return list(query_set), None

        # 分页查询
        paginator = Paginator(query_set, size)
        try:
            finish_set = list(paginator.page(page).object_list)
        except EmptyPage:
            return {"count": count, "page": int(page), "size": int(size), "list": []}, None

        return {"count": count, "page": int(page), "size": int(size), "list": finish_set}, None

    @staticmethod
    def del_api(pk: int = None, search_params: dict = None, **kwargs):
        """删除系统API"""
        pk, err = force_transform_type(variable=pk, var_type="int")
        search_params, err = force_transform_type(variable=search_params, var_type="only_dict")
        # 构建ORM
        if pk:
            api_obj = RoleApi.objects.filter(pk=pk)
        elif search_params:
            api_obj = RoleApi.objects.filter(**search_params)
        else:
            return None, None
        # 删除
        total = api_obj.count()
        if total < 1:
            return None, "没有可修改的数据"
        # api_obj.delete()
        api_obj.update(is_delete=1)

        return None, None

    @staticmethod
    def add_api(params: dict = None, **kwargs):
        """新增系统API"""
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=["route|str", "method|str", "module|str", "name|str", "is_using|int", "is_open_api|int", "description|str"],
        )

        # 参数校验
        for key in ["route", "method", "name"]:
            if params.get(key):
                continue
            return None, key + "必须填写"

        # 重复校验
        if RoleApi.objects.filter(route=params["route"]).first():
            return None, "该路由已经创建，请勿重复创建"

        # 创建数据
        try:
            RoleApi.objects.create(**params)
        except Exception as e:
            return None, "msg:" + str(e).replace(":", " ").replace(";", "  ") + ";tip:新增异常，请稍后再试"

        return None, None

    @staticmethod
    def edit_api(pk: int, params: dict = None, **kwargs):
        """编辑系统API"""
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=["route|str", "method|str", "name|str", "is_open_api|int", "description|str", "is_using|int"]
        )

        # 重复校验
        if not RoleApi.objects.filter(id=pk).first():
            return None, "数据不存在,无法修改"

        # 创建数据
        try:
            RoleApi.objects.filter(id=pk).update(**params)
        except Exception as e:
            return None, "msg:" + str(e).replace(":", " ").replace(";", "  ") + ";tip:新增异常，请稍后再试"

        return None, None

    @staticmethod
    def __get_system_apis():
        """获取系统API"""
        api_gator = GetSystemApis()
        return api_gator.get_apis(), None

    def sync_system_apis(self):
        """同步系统API"""
        sync_lock_key = "sync-system-api-clock"
        if self.redis_conn.get(sync_lock_key):
            return None, "msg:正在同步;tip:正在同步，稍后再试"
        else:
            self.redis_conn.set(sync_lock_key, 1, 100)
            api_gator = GetSystemApis()
            system_apis = api_gator.get_apis()
            database_apis = RoleApi.objects.values("route").all()
            database_apis_hash = {i["route"]: i for i in database_apis}

            for api_map in system_apis:
                if database_apis_hash.get(api_map["api"]):
                    pass
                else:
                    # 正则获取模型名称
                    try:
                        module_patt = "(^[/]?api[/]?)([a-z]*)"
                        api_str, module = re.match(module_patt, api_map["api"]).groups()
                    except Exception as e:
                        module = ""

                    # API入库
                    api_orm_obj = RoleApi(
                        module="xj_" + module,
                        route=api_map["api"],
                        method=api_map["method"],
                        name=api_map["name"]
                    )
                    api_orm_obj.save()
            self.redis_conn.delete(sync_lock_key)
            return None, None
