# encoding: utf-8
"""
@project: djangoModel->user_permission_service
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 用户权限服务
@created_time: 2022/8/23 9:33
"""

from django.core.paginator import Paginator, EmptyPage
from django.db import transaction
from django.db.models import F

from ..models import RolePermission, RoleMenu, RoleApi, Role
from ..utils.custom_tool import format_params_handle, force_transform_type


# 权限值服务
class PermissionValueService():
    type_to_primary_key = {
        "API": "api_id",
        "MENU": "menu_id",
        "DATA": "data_set_id"
    }

    type_to_values = {
        "API": [
            "id", "role_id", "type", "description", "permission_created_time", "role_role", "role_role_name", "role_parent_role_id", "role_user_group",
            "api_id", "api_module", "api_route", "api_name", "api_method", "filter_filed_list", "remove_filed_list", "default_value_dict", "allow_values_dict",
            "output_filter_filed_list", "output_remove_filed_list",
        ],
        "MENU": [
            "id", "role_id", "type", "description", "permission_created_time", "role_role", "role_role_name", "role_parent_role_id", "role_user_group",
            "menu_id", "menu_name", "menu_route", "menu_link", "menu_level", "menu_parent_id",

        ],
        "DATA": [
            "id", "role_id", "type", "description", "permission_created_time", "role_role", "role_role_name", "role_parent_role_id", "role_user_group",
            "data_set_id", "data_set_type",
        ]
    }

    @staticmethod
    def get_permission(params: dict = None, need_Pagination=True, only_first=False, max_length: "int|bool" = 100, **kwargs):
        """
        权限列表
        :param max_length: 允许查询的最大条数
        :param only_first: 是否进查询一条
        :param params: 查询参数
        :param need_Pagination: 是否分页
        :return: data, err
        """
        # --------------------- section 参数处理 start ------------------------------
        params, err = force_transform_type(variable=params, var_type="only_dict", default={})
        kwargs, err = force_transform_type(variable=kwargs, var_type="only_dict", default={})
        params.update(kwargs)
        page, err = force_transform_type(variable=params.pop("page", 1), var_type="int", default=1)
        size, err = force_transform_type(variable=params.pop("size", 10), var_type="int", default=10)
        sort = params.pop("sort", "-id")
        sort = sort if sort in [
            "permission_created_time", "-permission_created_time", "id", "-id"
        ] else "-id"

        need_Pagination, err = force_transform_type(variable=need_Pagination, var_type="bool", default=False)
        params = format_params_handle(
            param_dict=params,
            is_remove_empty=True,
            split_list=["id_list"],
            filter_filed_list=[
                "id|int",
                "id_list|list_int",
                "role_id|int",
                "role_id_list|list_int",
                "type|str",
                "api_id|int",
                "menu_id|int",
                "forbidden_menu|int",
                "api_route",
                "menu_route",
                "menu_level",
                "api_name"
            ],
            alias_dict={"id_list": "id__in", "role_id_list": "role_id__in"}
        )
        # --------------------- section 参数处理 end   ------------------------------

        # --------------------- section 构架ORM start ------------------------------
        query_set = RolePermission.objects.extra(select={"permission_created_time": 'DATE_FORMAT(role_permission_v2.created_time, "%%Y-%%m-%%d %%H:%%i:%%s")'})
        select_values = PermissionValueService.type_to_values.get(params.get("type"), [])
        # 联表查询，防止无用的联表查询。
        if params.get("type") == "API":
            query_set = query_set.annotate(
                api_module=F("api__module"),
                api_route=F("api__route"),
                api_name=F("api__name"),
                api_method=F("api__method"),
                api_is_delete=F("api__is_delete"),
            ).filter(api_is_delete=0)
        elif params.get("type") == "MENU":
            query_set = query_set.annotate(
                menu_parent_id=F("menu__parent_id"),
                menu_name=F("menu__name"),
                menu_route=F("menu__route"),
                menu_link=F("menu__link"),
                menu_level=F("menu__level"),
                menu_is_delete=F("menu__is_delete"),
            ).filter(menu_is_delete=0)

        # 查询
        query_set = query_set.annotate(
            role_role=F("role__role"),
            role_role_name=F("role__role_name"),
            role_parent_role_id=F("role__parent_role_id"),
            role_user_group=F("role__user_group"),
            role_is_delete=F("role__is_delete")
        ).filter(role_is_delete=0).filter(**params).values(*select_values)
        query_set = query_set.order_by(sort)
        count = query_set.count()

        # 仅仅查询第一条
        if only_first:
            return query_set.first(), None

        # 不分页查询
        if not need_Pagination and (not max_length or count <= max_length):
            return list(query_set), None

        # 分页查询
        paginator = Paginator(query_set, size)
        try:
            finish_set = list(paginator.page(page).object_list)
        except EmptyPage:
            return {"count": count, "page": page, "size": size, "list": []}, None

        return {"count": count, "page": page, "size": size, "list": finish_set}, None
        # --------------------- section 构架ORM end   ------------------------------

    @staticmethod
    def add_permission(params: dict = None, **kwargs):
        """
        添加权限值
        :param params: 添加参数
        :param kwargs: 最省参数
        :return: data,err
        """
        params, err = force_transform_type(variable=params, var_type="only_dict", default={})
        kwargs, err = force_transform_type(variable=kwargs, var_type="only_dict", default={})
        params.update(kwargs)
        # 参数过滤
        try:
            params = format_params_handle(
                param_dict=params,
                is_remove_empty=True,
                is_validate_type=True,
                filter_filed_list=[
                    "type|str",
                    "role_id|int",
                    "api_id|int",
                    "menu_id|int",
                    "data_set_id|int",
                    "data_set_type|str",
                    "filter_filed_list|list",
                    "remove_filed_list|list",
                    "default_value_dict|only_dict",
                    "allow_values_dict|only_dict",
                    "output_filter_filed_list|list",
                    "output_remove_filed_list|list",
                    "description|str"
                ],
                split_list=["filter_filed_list", "remove_filed_list", "output_filter_filed_list", "output_remove_filed_list"]
            )
            if not params.get("type") or not params.get("type") in [i[0] for i in RolePermission.type_choices]:
                return None, "msg:不是一个有效的权限类型;tip:不是一个有效的权限类型"

            if not params.get("role_id") or not Role.objects.filter(id=params.get("role_id"), is_delete=0).first():
                return None, "msg:不是一个有效的角色ID（role_id）;tip:不是一个有效的角色ID"

            if params.get("type") == "API" and (not params.get("api_id") or not RoleApi.objects.filter(id=params.get("api_id"), is_delete=0).first()):
                return None, "msg:不是一个有效的接口ID（api_id）;tip:不是一个有效的接口ID"

            if params.get("type") == "MENU" and (not params.get("menu_id") or not RoleMenu.objects.filter(id=params.get("menu_id"), is_delete=0).first()):
                return None, "msg:不是一个有效的菜单ID（menu_id）;tip:不是一个有效的菜单ID"

            if params.get("type") == "DATA" and (not params.get("data_set_type") or not params.get("data_set_id")):
                return None, "msg:参数错误data_set_id或者data_set_type不正确;tip:参数错误"

        except ValueError as e:
            return None, str(e)

        search_params = format_params_handle(
            param_dict=params,
            filter_filed_list=["type|str", "role_id|int", "api_id|int", "menu_id|int", "data_set_id|int", "data_set_type|str"],
        )

        # 检测是否是重复绑定
        exists = RolePermission.objects.filter(**search_params).exists()
        if exists:
            return None, "该权限已经绑定，请勿重复绑定"

        # 构建ORM
        try:
            permission_value_obj = RolePermission(**params)
            permission_value_obj.save()
        except Exception as e:
            return None, "msg:" + str(e).replace(":", " ").replace(";", " ") + ";tip:修改失败，请及时联系管理人员"

        return {"id": permission_value_obj.id}, None

    @staticmethod
    def del_permission(pk: int = None, search_params: dict = None):
        """
        删除权限值
        :param pk: 删除ID
        :param search_params: 批量删除，检索条件字典
        :return: data,err
        """
        # ---------------------- section 参数过滤 start ---------------------------------
        pk, err = force_transform_type(variable=pk, var_type="int")
        search_params, err = force_transform_type(variable=search_params, var_type="only_dict", default={})
        search_params = format_params_handle(
            param_dict=search_params,
            filter_filed_list=["id|int", "id_list|list_int", "api_id|int", "menu_id|int", "role_id|int"]
        )
        # ---------------------- section 参数过滤 end   ---------------------------------

        # ---------------------- section 构构建ORM start ---------------------------------
        if pk:
            instance = RolePermission.objects.filter(id=pk)
        elif search_params:
            instance = RolePermission.objects.filter(**search_params)
        else:
            return None, "msg:参数错误;tip:找不到要删除的数据"

        if instance.count() < 1:
            return None, "不存在该数据"

        if instance:
            instance.delete()
        # ---------------------- section 构构建ORM end   ---------------------------------

        return None, None

    @staticmethod
    def edit_permission(pk: int = None, search_params: dict = None, params: dict = None, **kwargs):
        """
        编辑权限值
        :param pk: 修改数据主键
        :param search_params: 检索数据字典
        :param params: 修改的参数
        :return: data, err
        """
        # --------------------- section 类型校验 start ------------------------------
        params, err = force_transform_type(variable=params, var_type="only_dict", default={})
        kwargs, err = force_transform_type(variable=kwargs, var_type="only_dict", default={})
        params.update(kwargs)
        pk, err = force_transform_type(variable=pk, var_type="int")
        search_params, err = force_transform_type(variable=search_params, var_type="only_dict", default={})
        # --------------------- section 类型校验 end   ------------------------------

        # --------------------- section 参数处理 start ------------------------------
        search_params = format_params_handle(
            param_dict=search_params,
            is_remove_empty=True,
            filter_filed_list=["id_list|list_int", "type|str", "api_id|int", "menu_id|int", "role_id|int"],
            alias_dict={"id_list": "id__in"}
        )
        try:
            params = format_params_handle(
                param_dict=params,
                is_remove_empty=True,
                is_validate_type=True,
                filter_filed_list=[
                    "type|str",
                    "api_id|int",
                    "role_id|int",
                    "filter_filed_list|list",
                    "remove_filed_list|list",
                    "default_value_dict|only_dict",
                    "allow_values_dict|only_dict",
                    "output_filter_filed_list|list",
                    "output_remove_filed_list|list",
                    "menu_id|int",
                    "forbidden_menu|int",
                    "description|str"
                ],
                split_list=["filter_filed_list", "remove_filed_list", "output_filter_filed_list", "output_remove_filed_list"]
            )
            if not params.get("type") or not params.get("type") in [i[0] for i in RolePermission.type_choices]:
                return None, "msg:不是一个有效的权限类型;tip:不是一个有效的权限类型"

            if params.get("type") == "API" and (not params.get("api_id") or not RoleApi.objects.filter(id=params.get("api_id")).first()):
                return None, "msg:不是一个有效的接口ID;tip:不是一个有效的接口ID"

            if params.get("type") == "MENU" and (not params.get("menu_id") or not RoleMenu.objects.filter(id=params.get("menu_id")).first()):
                return None, "msg:不是一个有效的菜单ID;tip:不是一个有效的菜单ID"
        except ValueError as e:
            return None, str(e)
        # --------------------- section 参数处理 end   ------------------------------

        # ------------------------------ section 构建ORM start --------------------------------------
        if pk:
            instance = RolePermission.objects.filter(id=pk)
        elif search_params:
            instance = RolePermission.objects.filter(**search_params)
        else:
            return None, "msg:没有可修改的数据;tip:提交错误"
        # 编辑
        try:
            instance.update(**params)
        except Exception as e:
            return None, "msg:编辑权限错误：" + str(e).replace(":", " ").replace(";", " ") + ";tip:修改错误，请联系管理员"
        # ------------------------------ section 构建ORM end   --------------------------------------
        return None, None

    @staticmethod
    def batch_bind_permission(role_id: int = None, permission_type: str = None, permission_param_list: list = None):
        """
        批零绑定
        :param role_id: 绑定的角色ID
        :param permission_type: 绑定权限的类型
        :param permission_param_list: 绑定列表
        :return: data,err
        """
        permission_type_key_name = PermissionValueService.type_to_primary_key.get(permission_type)
        # -------------------------- section 处理绑定权限列表 start ------------------------------------
        bind_role_permission_hash = {i[permission_type_key_name]: i for i in permission_param_list if isinstance(i, dict) and i.get(permission_type_key_name)}
        bind_role_permission_keys = list(bind_role_permission_hash.keys())
        # -------------------------- section 处理绑定权限列表 end   ------------------------------------

        # -------------------------- section 获取已绑定的权限并进行处理 start ------------------------------------
        current_role_permissions, err = PermissionValueService.get_permission(
            role_id=role_id,
            type=permission_type,
            need_Pagination=False,
            max_length=False
        )
        # 建立hash方便后面获取，获取主键列表，进行差集计算
        current_role_permission_hash = {i.get(permission_type_key_name): i for i in current_role_permissions}
        role_permission_keys = list(current_role_permission_hash.keys())
        # -------------------------- section 获取已绑定的权限并进行处理 end   ------------------------------------
        need_bind_permission = list(set(bind_role_permission_keys).difference(set(role_permission_keys)))
        need_unbind_permission = list(set(role_permission_keys).difference(set(bind_role_permission_keys)))
        # -------------------------- section 绑定与取消绑定 start ------------------------------------
        sid = transaction.savepoint()
        for permission_key in need_bind_permission:
            data, err = PermissionValueService.add_permission(
                type=permission_type,
                role_id=role_id,
                params=bind_role_permission_hash.get(permission_key)
            )
            # if err:
            #     transaction.savepoint_rollback(sid)
            #     return None, err

        for permission_key in need_unbind_permission:
            print(permission_key)
            pk = current_role_permission_hash.get(permission_key).get("id")
            if not pk:
                continue
            data, err = PermissionValueService.del_permission(pk=pk)
            # if err:
            #     transaction.savepoint_rollback(sid)
            #     return None, err

        transaction.savepoint_commit(sid)
        # -------------------------- section 绑定与取消绑定 start ------------------------------------
        return None, None
