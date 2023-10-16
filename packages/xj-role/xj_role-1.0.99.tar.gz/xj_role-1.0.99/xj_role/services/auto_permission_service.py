# encoding: utf-8
"""
@project: djangoModel->user_permission_service
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 用户权限服务
@created_time: 2022/8/23 9:33
"""
from typing import AnyStr, List, Dict, Tuple, Any, SupportsInt, SupportsFloat

from django.core.paginator import Paginator
from django.db.models import F

from xj_role.utils.model_handle import format_params_handle
from ..models import RolePermission
from ..services.role_service import RoleTreeService, RoleService
from ..services.permission_service import PermissionService
from ..utils.j_dict import JDict
from ..utils.j_recur import JRecur


# 权限值服务
class AutoPermissionValueService:
    @staticmethod
    def auto_filter_by_permission(source_list: list, user_id: int, module: str, feature_list: list):
        """ 按权限自动过滤数据，并返回过滤结果
        @param source_list 被过滤的来源数据
        @param user_id 用户ID。用于甄别角色后拉取相关权限
        @param module 模块名，必传。
        @param feature_list 功能列表，必传。
        """
        # print("> auto_filter_by_permission:", len(source_list), user_id, module, feature_list)

        # ==================== 1、先通过用户ID拿到所属角色权限树 ====================
        permission_tree, error_text = PermissionService.user_permission_tree(user_id=user_id, module=module,
                                                                             feature_list=feature_list)
        # print("> permission_tree:", permission_tree)

        # ==================== 2、再问权限树中哪些角色可操作 ====================
        user_role_list = RoleService.user_role_list(user_id=user_id)
        # print("> user_role_list:", user_role_list)
        role_forest = []
        inside_role_dict = {}
        for it in user_role_list:
            tree, error_text = RoleTreeService.role_tree(role_id=it.get('role_id', None))
            role_forest.append(tree)
            inside_role_dict[tree['id']] = 1
            # parent_role_list = JRecur
        # print("> role_tree:", role_forest)

        # ==================== 3、再问权限树中哪些用户可操作 ====================
        inside_role_list = [it for it in inside_role_dict]
        inside_user_list = [it['user_id'] for it in RoleService.user_list_by_roles(inside_role_list)]
        # print("> inside_role_list:", inside_role_list)
        # print("> inside_user_list:", inside_user_list)
        children_role_list = JRecur.get_value_in_forest(source_forest=role_forest, field='id')
        children_user_list = [it['user_id'] for it in RoleService.user_list_by_roles(children_role_list)]
        # print("> children_role_list:", children_role_list)
        # print("> children_user_list:", children_user_list)

        # ==================== 4、遍历来源看看是否有权限 ====================
        result_list = []
        # permission_tree = JDict(permission_tree)  # 与当前用户有关的权限值
        for item in source_list:
            # print("> item", item)
            if AutoPermissionValueService.__is_ban_other_role_operate(item, permission_tree, module, feature_list):
                 continue
            result_list.append(item)


        # ==================== 2、再过滤掉不可查看的类别（即同级、子级、父级、外级全禁止的） ====================

        # ==================== 3、再去掉有access_level(访问级别)的信息 ====================

        # ==================== 4、逐个类别查看是否有允许查看和用户ID列表 ====================

        # ban_user_list = []  # 允许读的用户列表
        # allow_user_list = []  # 禁止读的用户列表
        # if permission_tree.GROUP_PARENT and permission_tree.GROUP_PARENT.ban_view.upper() == "Y":
        #     ban_user_list.extend(permission_tree.GROUP_PARENT.user_list)
        # else:
        #     allow_user_list.extend(permission_tree.GROUP_PARENT.user_list if permission_tree.GROUP_PARENT else [])
        #
        # if permission_tree.GROUP_CHILDREN and permission_tree.GROUP_CHILDREN.ban_view.upper() == "Y":
        #     ban_user_list.extend(permission_tree.GROUP_CHILDREN.user_list)
        # else:
        #     allow_user_list.extend(permission_tree.GROUP_CHILDREN.user_list if permission_tree.GROUP_CHILDREN else [])
        #
        # if permission_tree.GROUP_INSIDE and permission_tree.GROUP_INSIDE.ban_view.upper() == "Y":
        #     ban_user_list.extend(permission_tree.GROUP_INSIDE.user_list)
        # else:
        #     allow_user_list.extend(permission_tree.GROUP_INSIDE.user_list if permission_tree.GROUP_INSIDE else [])

        # if not permission_tree.GROUP_ADMINISTRATOR and not permission_tree.GROUP_MANAGER:
        #     if permission_tree.GROUP_OUTSIDE and permission_tree.GROUP_OUTSIDE.ban_view.upper() == "Y":
        #         params['user_id__in'] = allow_user_list
        #     else:
        #         params["user_id__not_in"] = ban_user_list
        # else:
        #     params["is_admin"] = True

        # print("> ThreadListAPIView params:", params)
        # print("> ThreadListAPIView allow_user_list, ban_user_list:", allow_user_list, ban_user_list)

        return result_list

    # 判断禁止权限值
    def __is_ban_other_role_operate(item, permission_tree, module, featrue_list, ):
        it = JDict(item)
        permission_tree = JDict(permission_tree)
        for ff in featrue_list:
            permission_value = permission_tree[module] and permission_tree[module][ff] and permission_tree[module][ff][it.category_value]
            # print("> permission_value", it.id, it.category_value, permission_value)
            if permission_value:
                # print("> permission_value", permission_value)
                # 按外人操作权限
                if ff == 'OTHER_ROLE_OPERATE':
                    if permission_value.ROLE_CHILDREN.ban_view == 'Y':
                        # result_list.pop(index)
                        # print("> 删除", it.id)
                        return True
        return False
