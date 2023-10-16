# encoding: utf-8
"""
@project: djangoModel->permission_base
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 权限基类
@created_time: 2023/6/28 16:37
"""


class PermissionBase:
    class PermissionType:
        DATA = "DATA"
        API = "API"
        MENU = "MENU"
