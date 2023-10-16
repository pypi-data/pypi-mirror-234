# encoding: utf-8
"""
@project: djangoModel->role_api
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 角色API
@created_time: 2022/9/2 15:38
"""
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from ..services.permission_service import PermissionValueService
from ..services.role_service import RoleService, RoleTreeService
from ..utils.custom_response import util_response
from ..utils.custom_tool import request_params_wrapper


class RoleAPIView(APIView):

    @api_view(["GET"])
    @request_params_wrapper
    def user_role_users(self, *args, request_params, **kwargs):
        """查询属于该角色的用户列表"""
        data, err = RoleService.user_role_users(
            params=request_params,
            is_subtree=request_params.get("is_subtree"),
            without_user_info=request_params.get("without_user_info"),
        )
        if err:
            return util_response(err=2000, msg=err)
        return util_response(data=data)

    @api_view(["GET"])
    @request_params_wrapper
    def tree(self, *args, request_params={}, **kwargs):
        """角色树接口"""
        res, err = RoleTreeService.role_tree(
            role_id=request_params.get("role_id", 0),
            role_key=request_params.get("role_key", None),
            params=request_params
        )
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=res)

    @api_view(["GET"])
    @request_params_wrapper
    def list(self, *args, request_params={}, **kwargs):
        """角色列表"""
        data, err = RoleService.get_role_list(
            params=request_params,
            need_pagination=True,
            filter_fields=request_params.pop("filter_fields", None),
            only_first=request_params.pop("only_first", False),
            get_tree=request_params.pop("get_tree", False),
        )
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @request_params_wrapper
    def put(self, *args, request_params={}, **kwargs):
        # 角色 修改接口
        request_params.setdefault("id", kwargs.get("role_id", None))
        data, err = RoleService.edit_role(request_params)
        if err:
            return util_response(err=1000, msg=err)
        # 联动绑定权限
        role_id = request_params.get("id") or request_params.get("role_id")
        permission_type = request_params.get("type", None) or request_params.get("permission_type", None)
        permission_param_list = request_params.get("permission_param_list", None)
        if role_id and isinstance(permission_type, str) and isinstance(permission_param_list, list):
            permission_data, permission_err = PermissionValueService.batch_bind_permission(
                permission_type=permission_type,
                role_id=role_id,
                permission_param_list=permission_param_list
            )
            if err:
                return util_response(err=1001, msg=permission_err)
        return util_response(data=data)

    @request_params_wrapper
    def post(self, *args, request_params={}, **kwargs):
        # 角色 添加接口
        data, err = RoleService.add_role(request_params)
        if err:
            return util_response(err=1000, msg=err)

        # 联动绑定权限
        role_id = data.get("id", None)
        permission_type = request_params.get("type", None)
        permission_param_list = request_params.get("permission_param_list", None)
        if role_id and isinstance(permission_type, str) and isinstance(permission_param_list, list):
            permission_data, permission_err = PermissionValueService.batch_bind_permission(
                permission_type=permission_type,
                role_id=role_id,
                permission_param_list=permission_param_list
            )
            if err:
                return util_response(err=1001, msg=permission_err)

        return util_response(data=data)

    @request_params_wrapper
    def delete(self, *args, request_params={}, **kwargs):
        # 角色 删除接口
        id = request_params.get("id", None) or kwargs.get("role_id")
        if not id:
            return util_response(err=1000, msg="id 必传")
        data, err = RoleService.del_role(id)
        if err:
            return util_response(err=1001, msg=err)
        return util_response(data=data)
