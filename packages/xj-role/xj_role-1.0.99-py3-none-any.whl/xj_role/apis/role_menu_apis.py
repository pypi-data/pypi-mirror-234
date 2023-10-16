# encoding: utf-8
"""
@project: djangoModel->role_menus
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 系统API相关接口
@created_time: 2023/6/15 11:07
"""
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from xj_role.services.role_service import RoleService
from ..services.role_nemus_services import RoleMenuServices
from ..utils.custom_response import util_response
from ..utils.custom_tool import request_params_wrapper, format_params_handle
from ..utils.user_wrapper import user_authentication_force_wrapper


class RoleMenuAPIView(APIView):

    @api_view(["POST"])
    @user_authentication_force_wrapper
    @request_params_wrapper
    def add_menu(self, *args, request_params, **kwargs):
        data, err = RoleMenuServices.add_menu(params=request_params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @api_view(["DELETE"])
    @user_authentication_force_wrapper
    @request_params_wrapper
    def del_menu(self, *args, request_params, **kwargs):
        pk = kwargs.get("pk") or request_params.get("id")
        data, err = RoleMenuServices.del_menu(pk=pk)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @api_view(["PUT"])
    @user_authentication_force_wrapper
    @request_params_wrapper
    def edit_menu(self, *args, request_params, **kwargs):
        pk = kwargs.get("pk") or request_params.get("pk") or request_params.get("id") or request_params.get("menu_id")
        data, err = RoleMenuServices.edit_menu(pk=pk, params=request_params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @api_view(["GET"])
    @user_authentication_force_wrapper
    @request_params_wrapper
    def get_menu(self, *args, request_params, **kwargs):
        data, err = RoleMenuServices.get_menu(
            params=request_params,
            only_first=request_params.pop("only_first", False),
            get_tree=request_params.pop("get_tree", False)
        )

        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @api_view(["GET"])
    @user_authentication_force_wrapper
    @request_params_wrapper
    def get_my_menu(self, *args, request_params, user_info, **kwargs):
        """
        查询个人的菜单列表
        :param request_params: 请求参乎上
        :param user_info: 用户角色
        :return: response
        """
        # 获取角色信息
        user_id = user_info.get("user_id")
        role_info, err = RoleService.get_role_list(
            params={"user_id": user_id},
            need_pagination=False
        )
        search_params = format_params_handle(
            param_dict=request_params,
            filter_filed_list=[
                "page|int", "size|int", "sort|str"],
        )
        search_params["role_id_list"] = [i["role_id"] for i in role_info]

        # 查询当前角色的菜单
        data, err = RoleMenuServices.get_menu(
            only_first=request_params.pop("only_first", False),
            get_tree=request_params.pop("get_tree", False),
            pagination=request_params.pop("need_pagination", False),
            filter_fields=request_params.pop("filter_fields", None),
            params=search_params
        )

        # 返回数据
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)
