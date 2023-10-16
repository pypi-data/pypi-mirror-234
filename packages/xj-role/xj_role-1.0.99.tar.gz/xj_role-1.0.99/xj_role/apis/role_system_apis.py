# encoding: utf-8
"""
@project: djangoModel->role_apis
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 系统API相关接口
@created_time: 2023/6/15 11:07
"""
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from ..services.role_apis_services import RoleApiServices
from ..utils.custom_response import util_response
from ..utils.custom_tool import request_params_wrapper


class RoleApisAPIView(APIView):

    @api_view(["POST"])
    @request_params_wrapper
    def add_api(self, *args, request_params, **kwargs):
        data, err = RoleApiServices.add_api(params=request_params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @api_view(["DELETE"])
    @request_params_wrapper
    def del_api(self, *args, request_params, **kwargs):
        pk = kwargs.get("pk") or request_params.get("id")
        data, err = RoleApiServices.del_api(pk=pk)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @api_view(["PUT"])
    @request_params_wrapper
    def edit_api(self, *args, request_params, **kwargs):
        pk = kwargs.get("pk") or request_params.get("pk") or request_params.get("id")
        data, err = RoleApiServices.edit_api(pk=pk, params=request_params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @api_view(["GET"])
    @request_params_wrapper
    def get_apis(self, *args, request_params, **kwargs):
        data, err = RoleApiServices.get_apis(
            params=request_params,
            only_first=request_params.pop("only_first", False)
        )

        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @api_view(["GET"])
    @request_params_wrapper
    def sync_system_apis(self, *args, **kwargs):
        app = RoleApiServices()
        data, err = app.sync_system_apis()
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)
