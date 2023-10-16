# encoding: utf-8
"""
@project: djangoModel->group_api
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 分组api
@created_time: 2022/9/5 11:48
"""
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from ..services.user_group_service import UserGroupService
from ..utils.custom_response import util_response
from ..utils.custom_tool import request_params_wrapper, format_params_handle
from ..utils.user_wrapper import user_authentication_force_wrapper


class GroupAPIView(APIView):
    @api_view(["POST"])
    @user_authentication_force_wrapper
    @request_params_wrapper
    def get_user_ids_by_group(self, *args, request_params=None, user_info=None, **kwargs):
        group_id = request_params.get("user_group_id") or kwargs.get("user_group_id") or 0
        if not group_id:
            return util_response(err=1000, msg="user_group_id 必传")
        data, err = UserGroupService.get_user_ids_by_group(group_id)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @api_view(["GET"])
    @user_authentication_force_wrapper
    @request_params_wrapper
    def user_group_tree(self, *args, request_params=None, user_info=None, **kwargs):
        """用户分组树"""
        # 这句看起来有问题，用户所在组ID是由接口传入的，不安全， 20221006 by sieyoo
        user_group_id = request_params.get("user_group_id") or kwargs.get("user_group_id") or 0
        data, err = UserGroupService.get_user_group_tree(
            user_group_id,
            is_family_tree=True,
            params=request_params
        )
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @api_view(["GET"])
    @request_params_wrapper
    def group_tree_role(self, *args, request_params={}, **kwargs):
        """分组树 ==> 角色列表"""
        data, err = UserGroupService.group_tree_role(request_params)
        return util_response(data=data)

    @api_view(["GET"])
    @request_params_wrapper
    def group_tree_user(self, *args, request_params={}, **kwargs):
        """分组树 ==> 用户列表"""
        data, err = UserGroupService.group_tree_user(request_params)
        return util_response(data=data)

    @api_view(["GET"])
    @request_params_wrapper
    def in_group_users(self, *args, request_params={}, **kwargs):
        """
        根据用户组下面查询的用户信息API
        :param request_params: 解析请求参数
        :return: JsonResponse
        """
        if request_params is None:
            request_params = {}
        need_child = request_params.get("need_child") == 1 \
                     or request_params.get("need_child") == True \
                     or request_params.get("need_child") == "1" \
                     or request_params.get("need_child") == "true"

        request_params = format_params_handle(
            param_dict=request_params,
            filter_filed_list=["page", "size", "phone", "user_name", "full_name", "email", "group_id", "user_id", "user_group_id"],
            is_remove_empty=True,
        )

        data, err = UserGroupService.in_group_users(request_params, need_child)
        if err:
            return util_response(err=2000, msg=err)
        return util_response(data=data)

    @api_view(["GET"])
    @user_authentication_force_wrapper
    @request_params_wrapper
    def group_user_detail(self, *args, request_params=None, user_info=None, **kwargs):
        if request_params is None:
            request_params = {}
        if user_info is None:
            user_info = {}
        user_id = request_params.get("user_id") or user_info.get("user_id")
        data, err = UserGroupService.group_user_detail(user_id)
        if err:
            return util_response(err=2000, msg=err)
        return util_response(data=data)

    @api_view(["POST"])
    @user_authentication_force_wrapper
    @request_params_wrapper
    def group_user_add(self, *args, request_params=None, user_info=None, **kwargs):
        data, err = UserGroupService.group_user_add(request_params)
        if err:
            return util_response(err=2000, msg=err)
        return util_response(data=data)

    @api_view(["PUT", "POST"])
    @request_params_wrapper
    def group_user_edit(self, *args, request_params=None, **kwargs):
        data, err = UserGroupService.group_user_edit(request_params)
        if err:
            return util_response(err=2000, msg=err)
        return util_response(data=data)

    @api_view(["GET"])
    @request_params_wrapper
    def user_group_list(self, *args, request_params=None, **kwargs):
        # 用户组 列表接口
        data, err = UserGroupService.group_list(
            params=request_params,
            only_first=request_params.get("only_first", False)
        )
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @request_params_wrapper
    def put(self, *args, request_params=None, **kwargs):
        # 用户组 修改接口
        request_params.setdefault("id", kwargs.get("user_group_id", None))
        data, err = UserGroupService.edit_group(request_params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @request_params_wrapper
    def post(self, *args, request_params=None, **kwargs):
        # 用户组 添加接口
        data, err = UserGroupService.add_group(request_params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @request_params_wrapper
    def delete(self, *args, request_params=None, **kwargs):
        # 用户组 删除接口
        user_group_id = request_params.get("id", None) or kwargs.get("user_group_id")
        if not id:
            return util_response(err=1000, msg="id 必传")
        data, err = UserGroupService.del_group(user_group_id)
        if err:
            return util_response(err=1001, msg=err)
        return util_response(data=data)

    @request_params_wrapper
    def user_bind_groups(self, *args, request_params=None, **kwargs):
        # 用户组 修改接口
        user_id = request_params.get("user_id", None)
        group_list = request_params.get("group_list", None)
        data, err = UserGroupService.user_bind_groups(user_id, group_list)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    # @user_authentication_force_wrapper
    # @request_params_wrapper
    # def group_user_delete(self, *args, request_params=None, **kwargs):
    #     user_id = request_params.get("user_id", None)
    #     data, err = UserGroupService.group_user_delete(user_id)
    #     if err:
    #         return util_response(err=2000, msg=err)
    #     return util_response(data=data)
