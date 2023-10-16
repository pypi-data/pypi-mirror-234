# encoding: utf-8
"""
@project: djangoModel->user_auth
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 用户权限API
@created_time: 2022/8/23 9:16
"""
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from xj_role.services.role_service import RoleService
from ..services.permission_service import PermissionValueService
from ..utils.custom_response import util_response
from ..utils.custom_tool import request_params_wrapper, force_transform_type
from ..utils.user_wrapper import user_authentication_force_wrapper


class PermissionValueAPIView(APIView):
    """
    权限相关操作API，增删改查
    """

    @api_view(["GET", "POST"])
    @request_params_wrapper
    @user_authentication_force_wrapper
    def batch_bind_permission(self, *args, request_params, **kwargs):
        """批量绑定角色"""
        data, err = PermissionValueService.batch_bind_permission(
            permission_type=request_params.get("type"),
            role_id=request_params.get("role_id"),
            permission_param_list=request_params.get("permission_param_list")
        )
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @request_params_wrapper
    @user_authentication_force_wrapper
    def post(self, *args, request_params, **kwargs):
        """权限添加"""
        data, err = PermissionValueService.add_permission(params=request_params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @request_params_wrapper
    @user_authentication_force_wrapper
    def get(self, *args, request_params, user_info, **kwargs):
        # 列表
        # 是否查看自己的权限
        look_self, err = force_transform_type(variable=request_params.get("look_self", False), var_type="bool", default=False)
        request_params_copy = request_params.copy()
        if look_self:
            data, err = RoleService.get_role_list(
                params={"user_id": user_info.get("user_id")},
                need_pagination=False,
                filter_fields=["role_id", "user_id"]
            )
            if err:
                return util_response(err=1000, msg=err)
            request_params_copy.setdefault("role_id_list", [i["role_id"] for i in data])
            
        # 查询
        request_params.setdefault("id", kwargs.get("pk", None))
        data, err = PermissionValueService.get_permission(
            params=request_params_copy,
            need_Pagination=request_params_copy.get("need_Pagination", True),
            only_first=request_params_copy.get("only_first", False),
        )
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @request_params_wrapper
    @user_authentication_force_wrapper
    def delete(self, *args, request_params, **kwargs):
        """权限删除"""
        pk = request_params.get("id") or kwargs.get("pk", None)
        if not id:
            return util_response(err=1000, msg="permission_id 不可以为空")
        data, err = PermissionValueService.del_permission(pk=pk)

        if err:
            return util_response(err=1001, msg=err)
        return util_response(data=data)

    @request_params_wrapper
    @user_authentication_force_wrapper
    def put(self, *args, request_params, **kwargs):
        """权限修改"""
        pk = request_params.get("id") or kwargs.get("pk", None)
        if not pk:
            return util_response(err=1000, msg="id 不可以为空")

        data, err = PermissionValueService.edit_permission(pk=pk, params=request_params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)
