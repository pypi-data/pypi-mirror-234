# encoding: utf-8
"""
@project: djangoModel->service_register
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 对外开放服务调用注册白名单
@created_time: 2023/1/12 14:29
"""

import xj_role

# 对外服务白名单
from .services.role_service import RoleService
from .services.user_group_service import UserGroupService

register_list = [
    {
        # 绑定角色
        "service_name": "bind_role",
        "pointer": RoleService.user_bind_role
    },
    {
        # 移除绑定的角色
        "service_name": "user_remove_role",
        "pointer": RoleService.user_remove_role
    },
    {
        # 绑定部门
        "service_name": "bind_group",
        "pointer": UserGroupService.user_bind_group
    },
    {
        # 移除绑定部门
        "service_name": "user_remove_group",
        "pointer": UserGroupService.user_remove_group
    },
]


# 遍历注册
def register():
    for i in register_list:
        setattr(xj_role, i["service_name"], i["pointer"])


if __name__ == '__main__':
    register()
