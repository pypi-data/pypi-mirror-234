# _*_coding:utf-8_*_

from django.urls import re_path

from .apis.group_api import GroupAPIView
from .apis.permission_api import PermissionValueAPIView
from .apis.role_api import RoleAPIView
from .apis.role_menu_apis import RoleMenuAPIView
from .apis.role_system_apis import RoleApisAPIView
from .service_register import register

app_name = 'xj_role'

register()

# 应用路由
urlpatterns = [
    # 角色相关接口
    re_path(r'^list/?$', RoleAPIView.list, name="角色列表"),
    re_path(r'^tree/?$', RoleAPIView.tree, name="角色树"),
    re_path(r'^role/?(?P<id>\d+)?$', RoleAPIView.as_view(), name="角色 增加（post）/删除(delete)/修改(edit)"),
    re_path(r'^user_role_users/?$', RoleAPIView.user_role_users, name="角色下面的用户列表"),

    # 用户组相关的接口
    re_path(r'^group/?(?P<user_group_id>\d+)?$', GroupAPIView.as_view(), name="分组:增加（post）/删除(delete)/修改(edit)"),
    re_path(r'^user_group_list/?$', GroupAPIView.user_group_list, name="分组列表"),
    re_path(r'^get_user_ids_by_group/(?P<user_group_id>\d+)?$', GroupAPIView.get_user_ids_by_group, name="查询分组下的所有的用户ID"),
    re_path(r'^in_group_users/?$', GroupAPIView.in_group_users, name="分组里面所有的用户 用户列表,支持用户的搜索"),
    re_path(r'^user_group_users/?$', GroupAPIView.in_group_users, name="分组里面所有的用户 用户列表,支持用户的搜索"),
    re_path(r'^user_group_tree/?$', GroupAPIView.user_group_tree, name="分组树"),
    re_path(r'^group_tree_role/?$', GroupAPIView.group_tree_role, name="分组角色树"),
    re_path(r'^group_tree_user/?$', GroupAPIView.group_tree_user, name="分组用户树"),

    # 用户分组和用户角色的多对多映射关系
    re_path(r'^group_user_detail/?$', GroupAPIView.group_user_detail, name="查询用户详情，待删除，使用用户详情代替"),  # TODO 待删除
    re_path(r'^group_user_add/?$', GroupAPIView.group_user_add, name="添加用户，并当定用户关系,设计不合理需要重新规划"),  # TODO 待重写
    re_path(r'^group_user_edit/?$', GroupAPIView.group_user_edit, name="编辑用户的角色和权限"),
    # re_path(r'^bind_user_role/?$', GroupAPIView.bind_user_role, ),  # 用户角色那绑定 # TODO 待重写
    re_path(r'^bind_user_group/?$', GroupAPIView.user_bind_groups, name="用户批量绑定分组"),  # 用户分组绑定

    # 角色管理API相关
    re_path(r'^get_apis/?$', RoleApisAPIView.get_apis, name="获取API"),
    re_path(r'^add_api/?$', RoleApisAPIView.add_api, name="添加API"),
    re_path(r'^edit_api/?(?P<pk>\d+)?$', RoleApisAPIView.edit_api, name="编辑API"),
    re_path(r'^del_api/?(?P<pk>\d+)?$', RoleApisAPIView.del_api, name="删除API"),
    re_path(r'^sync_apis/?$', RoleApisAPIView.sync_system_apis, name="同步系统的API"),

    # 角色菜单管理接口
    re_path(r'^get_menu/?$', RoleMenuAPIView.get_menu, name="获取菜单"),
    re_path(r'^get_my_menu/?$', RoleMenuAPIView.get_my_menu, name="获取自己的菜单"),
    re_path(r'^add_menu/?$', RoleMenuAPIView.add_menu, name="添加菜单"),
    re_path(r'^edit_menu/?(?P<pk>\d+)?$', RoleMenuAPIView.edit_menu, name="编辑菜单"),
    re_path(r'^del_menu/?(?P<pk>\d+)?$', RoleMenuAPIView.del_menu, name="删除菜单"),

    # 角色权限相关
    re_path(r'^permission/?(?P<pk>\d+)?$', PermissionValueAPIView.as_view(), name="角色权限-CURD"),
    re_path(r'^batch_bind_permission/?$', PermissionValueAPIView.batch_bind_permission, name="角色批量绑定权限"),
]
