# encoding: utf-8
"""
@project: djangoModel->group_service
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 用户组（部门服务）
@created_time: 2022/9/5 11:33
"""

from django.core.paginator import Paginator, EmptyPage
from django.db import transaction
from django.db.models import F
from django.db.models import Q

from xj_user.services.user_service import UserService
from ..models import UserToGroup, RoleUserGroup, UserToRole
from ..services.role_service import RoleService
from ..utils.custom_tool import format_params_handle, parse_json, format_list_handle, force_transform_type, \
    filter_fields_handler
from ..utils.j_recur import JRecur
from ..utils.join_list import JoinList
from ..utils.utility_method import parse_integers

from orator import DatabaseManager
from decimal import Decimal
from config.config import JConfig

config = JConfig()
db_config = {
    config.get('main', 'driver', "mysql"): {
        'driver': config.get('main', 'driver', "mysql"),
        'host': config.get('main', 'mysql_host', "127.0.0.1"),
        'database': config.get('main', 'mysql_database', ""),
        'user': config.get('main', 'mysql_user', "root"),
        'password': config.get('main', 'mysql_password', "123456"),
        "port": config.getint('main', 'mysql_port', "3306")
    }
}
db = DatabaseManager(db_config)

# 用户组CURD服务
class UserGroupService(object):

    @staticmethod
    def add_group(params: dict):
        """
        添加部门
        :param params: 部门参数
        :return: None, err
        """
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=["group", "group_name", "parent_group_id", "description",
                               "manager_name", "manager_phone", "is_using", "sort"]
        )
        if not params:
            return None, "参数不能为空"
        res = RoleUserGroup.objects.filter(group=params.get("group")).exists()
        if res:
            return None, "组标签，必须唯一"
        if params.get("parent_group_id") == 0:
            params.pop("parent_group_id")
        instance = RoleUserGroup.objects.create(**params)
        return None, None

    @staticmethod
    def edit_group(params: dict):
        """
        用户分组编辑，可编辑参数："group", "group_name", "parent_group_id", "description"
        :param params: 编辑参数
        :return: None,err
        """
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=["id", "group", "group_name", "parent_group_id", "description",
                               "manager_name", "manager_phone", "is_using", "sort"]
        )
        id = params.pop("id", None)
        if not id:
            return None, "ID 不可以为空"
        if not params:
            return None, "没有可以修改的字段"
        res = RoleUserGroup.objects.filter(Q(group=params.get("group")), ~Q(id=id)).exists()
        if res:
            return None, "组标签，必须唯一"
        instance = RoleUserGroup.objects.filter(id=id)
        if params.get("parent_group_id") == 0:
            params.pop("parent_group_id")
        if params:
            instance.update(**params)
        return None, None

    @staticmethod
    def details_group(params: dict):
        """
        用户分组编辑，可编辑参数："group", "group_name", "parent_group_id", "description"
        :param params: 编辑参数
        :return: None,err
        """
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=["id", "group", "group_name", "parent_group_id", "description"]
        )
        id = params.pop("id", None)
        if not id:
            return None, "ID 不可以为空"
        instance = RoleUserGroup.objects.filter(id=id).first()
        if not instance:
            return None, "分组不存在"
        instance = instance.to_json()
        return instance, None

    @staticmethod
    def del_group(id: int):
        """
        删除用户的分组
        :param id: 分组的主键ID
        :return: None,err
        """
        if not id:
            return None, "ID 不可以为空"
        user_role_set = UserToGroup.objects.filter(user_group_id=id).exists()
        if user_role_set:
            return None, "该组织有绑定关系,无法删除"
        instance = RoleUserGroup.objects.filter(id=id)
        if instance:
            instance.delete()
        return None, None

    @staticmethod
    def group_list(params: dict, need_pagination: bool = True, only_first: bool = False, filter_fields: bool = None,
                   **kwargs):
        """
        用户的分组列表，分页查询。
        :param filter_fields: 过滤字段
        :param only_first: 仅仅查询第一条
        :param need_pagination: 是否需要分页查询
        :param params: 请求的
        :return: page_set,err
        """
        kwargs, is_pass = force_transform_type(variable=kwargs, var_type="dict", default={})
        params, is_pass = force_transform_type(variable=params, var_type="dict", default={})
        params.update(kwargs)
        need_pagination, is_pass = force_transform_type(variable=need_pagination, var_type="bool", default=True)
        only_first, is_pass = force_transform_type(variable=only_first, var_type="bool", default=False)
        page, is_pass = force_transform_type(variable=params.pop("page", 1), var_type="int", default=1)
        size, is_pass = force_transform_type(variable=params.pop("size", 10), var_type="int", default=10)
        sort = params.pop("sort", "-user_group_id")
        sort = sort if sort in ["user_group_id", "-user_group_id", "sort", "-sort"] else "-user_group_id"

        user_id = params.get("user_id", None)
        user_id_list = params.get("user_id_list", None)
        # 参数有效性处理
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=["id|int", "user_group_id|int", "user_id", "user_id_list",
                               "id_list|list_int", "group", "group_name", "parent_group_id|int",
                               "manager_name", "manager_phone", "is_using|int"],
            alias_dict={"group_name": "group_name__contains", "group": "group__contains", "user_id_list": "user_id__in",
                        "id_list": "id__in"},
            split_list=["user_id_list", "id_list"]
        )
        all_field_list = ["id", "user_group_id", "group", "group_name", "parent_group_id", "sort", "description",
                          "manager_name", "manager_phone", "is_using"]
        filter_fields = filter_fields_handler(input_field_expression=filter_fields, all_field_list=all_field_list)
        # sql查询数据
        if not (user_id or user_id_list):
            group_set = RoleUserGroup.objects.annotate(user_group_id=F("id")).filter(**params)
        else:
            filter_fields.append("user_id")  # 返回用户ID
            filter_fields.remove("sort")
            group_set = UserToGroup.objects.annotate(
                group=F("user_group__group"),
                group_name=F("user_group__group_name"),
                parent_group_id=F("user_group__parent_group_id"),
                description=F("user_group__description"),
            ).filter(**params)

        group_set = group_set.order_by(sort)
        group_list = group_set.values(*filter_fields)

        # 仅仅返回第一条
        if only_first:
            return group_list.first(), None

        # 返回全部，不分页
        total = group_set.count()
        if (not need_pagination and total <= 200) or (user_id or user_id_list):
            return list(group_list), None

        # 分页查询
        paginator = Paginator(group_list, size)
        try:
            finish_set = paginator.page(page)
        except EmptyPage:
            return {"page": int(page), "size": int(size), "count": int(total), "total": total, "list": []}, None

        return {"page": int(page), "size": int(size), "count": int(total), "total": total,
                "list": list(finish_set.object_list)}, None

    @staticmethod
    def get_user_ids_by_group(group_id):
        """
        根据用户组ID,获取该分组下面的所有用户ID列表
        :param group_id: 分组ID
        :return: data, err
        """
        user_obj = UserToGroup.objects.filter(user_group_id=group_id)
        user_list = []
        if user_obj:
            user_list = user_obj.values("user_id")
            user_list = [i['user_id'] for i in user_list]
        return user_list, None

    @staticmethod
    def in_group_users(params=None, need_child=False):
        """
        获取用户分组下用户列表
        :param params: 查询参数
        :param need_child:  是否查询子节点
        :return: data, err
        """
        if params is None:
            params = {}
        # 分页参数
        page = params.pop("page", 1)
        size = params.pop("size", 10)

        # 用户条件反查, 得到用user_id列表.
        user_search_params = format_params_handle(
            param_dict=params,
            filter_filed_list=["phone", "user_name", "full_name", "email"],
            is_remove_empty=True
        )
        if user_search_params:
            user_serv, err = UserService.user_list(params=user_search_params, need_Pagination=False,
                                                   is_strict_mode=False)
            params["user_id_list"] = [i["user_id"] for i in user_serv if i]

        # 是否需要子节点搜索
        user_group_id = params.get("user_group_id") or params.get("group_id")
        if need_child and user_group_id:
            group_id_tree, err = UserGroupService.get_user_group_tree(user_group_id)
            if err:
                return None, err
            params["user_group_id_list"] = JRecur.get_value_in_forest(group_id_tree)
            params.pop("group_id", None)
            params.pop("user_group_id", None)

        # 分组下面用户分页查询
        group_search_params = format_params_handle(
            param_dict=params,
            filter_filed_list=["group_id|int", "user_group_id|int", "user_group_id_list|list", "user_id|int",
                               "user_id_list|list"],
            alias_dict={"user_group_id_list": "user_group_id__in", "group_id": "user_group_id",
                        "user_id_list": "user_id__in"},
        )

        # 分组用户查询
        user_group_set = UserToGroup.objects.filter(**group_search_params).annotate(
            user_group_value=F("user_group__group"),
            user_group_name=F("user_group__group_name")
        ).values("user_id", "user_group_name", "user_group_value")
        total = user_group_set.count()
        paginator = Paginator(user_group_set, size)
        # 分页保护
        try:
            group_user_list = list(paginator.page(page).object_list)
        except EmptyPage:
            return {"total": total, "page": int(page), "size": int(size), "list": []}, None

        # 拼接用户信息
        user_serv, err = UserService.user_list(allow_user_list=list(set([it['user_id'] for it in group_user_list])),
                                               need_Pagination=False)
        group_user_list = JoinList(l_list=group_user_list, r_list=user_serv, l_key="user_id", r_key="user_id").join()

        # 由于数据迁移导致部门绑定的用户ID,用户表存在该用户的信息了,遍历做出提示
        for i in group_user_list:
            if i.get("user_name", None) is None:
                i["full_name"] = "--- 该用户不存在,请移除.然后重新绑定 ---"
                i["email"] = ""
                i["user_name"] = ""
                i["nickname"] = ""
                i["register_time"] = ""
                i["wechat_openid"] = ""

        return {"total": total, "page": int(page), "size": int(size), "list": group_user_list}, None

    @staticmethod
    def user_bind_group(user_id: int, group_id: int = None, group_value: str = None):
        """
        绑定用户与分组关系，即插入一条用户的分组映射关系
        :param group_value: 添加角色的value
        :param user_id: 用户ID
        :param group_id: 分组ID
        :return: None,err
        """
        # 如果存在role_value，则有限使用role_value查询添加的角色
        if not group_value is None:
            find_group_id = RoleUserGroup.objects.filter(group=group_value).values("id").first()
            group_id = find_group_id.get("id", None) if find_group_id else group_id

        if not user_id or not group_id:
            return None, "参数错误，user_id, group_id 必传"
        # 部门校验
        if not UserToGroup.objects.filter(user_group_id=group_id).first():
            return None, "该部门不存在"

        # 绑定部门
        try:
            user_group_set = UserToGroup.objects.filter(user_id=user_id, user_group_id=group_id).first()
            if not user_group_set:
                UserToGroup.objects.create(user_id=user_id, user_group_id=group_id)
            return None, None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def user_remove_group(user_id: int, group_id: int = None, group_value: str = None):
        """
        绑定用户与分组关系，即插入一条用户的分组映射关系
        :param group_value: 添加角色的value
        :param user_id: 用户ID
        :param group_id: 分组ID
        :return: None,err
        """

        # 如果存在role_value，则有限使用role_value查询添加的角色
        if not group_value is None:
            find_group_id = RoleUserGroup.objects.filter(group=group_value).values("id").first()
            group_id = find_group_id.get("id", None) if find_group_id else group_id

        # 参数介绍
        if not user_id or not group_id:
            return None, "参数错误，user_id, group_id 必传"

        # 移除部门
        try:
            user_group_set = UserToGroup.objects.filter(user_id=user_id, user_group_id=group_id).first()
            if user_group_set:
                UserToGroup.objects.filter(user_id=user_id, user_group_id=group_id).delete()
            return None, None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def user_bind_groups(user_id: int, group_list: list):
        """
        用户批量绑定用户的分组关系
        :param user_id: 被绑定用户ID
        :param group_list: 需要绑定的分组ID的 列表或逗号分割字符串，如果传空则表示清空选择。
        :return: None,err
        """
        # 如果传控制则表示
        if not group_list:
            UserToGroup.objects.filter(user_id=user_id).delete()
            return None, None
        group_list = parse_integers(group_list)
        # group_list = group_list.split(',') if isinstance(group_list, str) else group_list
        sid = transaction.savepoint()
        try:
            UserToGroup.objects.filter(user_id=user_id).delete()
            # 添加数据
            for group in group_list:
                data = {
                    "user_id": user_id,
                    "user_group_id": group
                }
                UserToGroup.objects.create(**data)
            transaction.clean_savepoints()
            return None, None
        except Exception as e:
            transaction.savepoint_rollback(sid)
            return None, str(e)

    @staticmethod
    def get_user_group_tree(group_id=None, is_family_tree=False, params: dict = None):
        """
        用戶分组树
        @param group_id 用户组ID，如果有则过滤用户组，没有会返回全部分组，请慎用。
        @param is_family_tree 是否返回整个家族数。
        @param params: 过滤树参数
        """
        params, err = force_transform_type(variable=params, var_type="only_dict", default={})
        filter_tree_params, err = JRecur.get_filter_tree_params(params=params)

        data_list = list(RoleUserGroup.objects.filter().annotate(name=F('group_name')).values(
            "id",
            "group",
            "group_name",
            "name",
            "parent_group_id",
            "description",
            "manager_name", "manager_phone", "is_using", "sort"
        ))
        group_tree = JRecur.create_forest(data_list, parent_key='parent_group_id')
        if group_id:
            group_tree = JRecur.filter_forest(
                source_forest=group_tree,
                find_key='id', find_value=group_id,
                is_family_tree=is_family_tree
            )

        elif filter_tree_params:
            for k, v in filter_tree_params.items():
                if not v:
                    continue
                group_tree = JRecur.filter_forest(group_tree, find_key=k, find_value=v, children_key='children')

        return group_tree, None

    @staticmethod
    def group_tree_role(params: dict):
        """
        分组角色树, 分组为树枝，角色为叶子
        :param params: 节点搜索参数
        :return: tree, err
        """
        group_id = params.get("group_id", 0)
        tree_data, err = UserGroupService.get_user_group_tree(group_id)
        if err:
            return None, err
        # 角色列表，并建立映射
        role_list, err = RoleService.get_role_list(
            params={},
            need_pagination=False
        )
        role_dict = {}
        for role in role_list:
            index = str(role['user_group_id'])
            if index not in role_dict.keys():
                role_dict[index] = []
            role_dict[index].append(role)

        # 统一名称字段，角色拼接到部门
        def parse_tree(tree, parent_group_id=None):
            for item in tree:
                if "children" not in item.keys():
                    item['children'] = []
                if len(item['children']) > 0:
                    parse_tree(item['children'], item["id"])

                if str(item['id']) in role_dict.keys():
                    role_list = role_dict[str(item['id'])]
                    for i in role_list:
                        i["name"] = i.get("role_name", "")
                        i["type"] = "role"
                        i["id"] = i.get("role_id")
                    item['children'].extend(role_dict[str(item['id'])])
                item["name"] = item.get("group_name", "")
                item["type"] = "group"
            return tree

        return parse_tree(parse_json(tree_data), 0), None

    @staticmethod
    def group_tree_user(params: dict):
        """
        分组用户树
        :param params: 搜索参数
        :return:
        """
        group_id = params.get("group_id", 0)
        tree_data, err = UserGroupService.get_user_group_tree(group_id)
        if err:
            return None, err
        user_group_obj = UserToGroup.objects
        if group_id:
            user_group_set = user_group_obj.filter(user_group_id=group_id)
        else:
            user_group_set = user_group_obj.all()
        user_group_dict = {str(item["user_id"]): str(item['user_group_id']) for item in
                           list(user_group_set.values())} if user_group_set else {}
        user_list, err = UserService.user_list({"id__in": user_group_dict.keys()}, None)
        group_user_dict = {}
        for user in user_list['list']:
            index = user_group_dict.get(str(user['user_id']), None)
            if not index:
                continue
            if index not in group_user_dict.keys():
                group_user_dict[index] = []
            user["group_id"] = index
            group_user_dict[index].append(user)

        def parse_tree(tree, parent_group_id=None):
            for item in tree:
                if "children" not in item.keys():
                    item['children'] = []
                if len(item['children']) > 0:
                    parse_tree(item['children'], item["id"])
                if str(item['id']) in group_user_dict.keys():
                    item['children'].extend(group_user_dict[str(item['id'])])
            return tree

        return parse_tree(parse_json(tree_data), 0), None

    @staticmethod
    def get_user_group_info(user_id: int = None, user_id_list: list = None, field_list=None, **kwargs):
        """
        获取指定用户的分组信息
        :param user_id: 用户id
        :param user_id_list: 用户的ID列表
        :param field_list: 字段过滤列表
        :return: 用户的部门列表，err
        """
        # 找不到可检索的用户，则直接返回
        if not user_id and not user_id_list:
            return [], None

        # 过滤字段合法性验证
        allow_field_list = ["user_id", 'user_group_id', 'group_name', 'group', 'description']
        field_list = format_list_handle(
            param_list=field_list or [],
            filter_filed_list=allow_field_list
        )
        field_list = allow_field_list if not field_list else field_list

        # query 对象构建
        user_group_obj = UserToGroup.objects.annotate(
            group_name=F("user_group__group_name"),
            group=F("user_group__group"),
            description=F("user_group__description"),
        ).values(*field_list)

        # 分情况检索数据
        if user_id:
            user_group_list = user_group_obj.filter(user_id=user_id)
            return list(user_group_list), None  # 返回用户的部门（分组）列表
        else:
            user_group_list = user_group_obj.filter(user_id__in=user_id_list)
            # 按照用户进行映射
            user_group_map = {}
            for item in list(user_group_list):
                if user_group_map.get(item['user_id']):
                    user_group_map[item['user_id']].append(item)
                else:
                    user_group_map[item['user_id']] = [item]
            return user_group_map, None  # 返回映射字典

    # @staticmethod
    # def group_user_delete(params):  # 建议删除,应该删除的用户的关系而不是删除这个用户,该操作比较危险
    #     user_serv, err = UserService.user_delete(params)
    #     if err:
    #         return None, err
    #     return None, None

    # ===============  用户分组和角色关系操作服务 start ===============
    @staticmethod
    def group_user_detail(user_id):  # 修改建议，放在用户模块里面，来角色问角色和分组列表
        from xj_user.services.user_detail_info_service import DetailInfoService
        user_serv_dict, err = DetailInfoService.get_detail(user_id)
        if err:
            return None, err
        user_serv = user_serv_dict
        user_group_serv = UserToGroup.objects.filter(user_id=user_id).values("user_id", 'user_group_id')
        user_group_dict = {item['user_group_id'] for item in user_group_serv}
        user_role_serv = UserToRole.objects.filter(user_id=user_id).values("user_id", 'role_id')
        user_role_dict = {item['role_id'] for item in user_role_serv}
        user_serv['user_group_list'] = list(user_group_dict)
        user_serv['user_role_list'] = list(user_role_dict)
        return user_serv, None

    @staticmethod
    def group_user_add(params):  # 更名或者单独起一个文件 方法这个方法
        # 用户角色部门绑定
        user_role_list = params.get('user_role_list', None)
        user_group_list = params.get('user_group_list', None)
        user_serv, err = UserService.user_add(params)  # 为什么要添加用户呢,用户和角色不应该分开吗
        if err:
            return None, err
        if user_group_list:
            UserGroupService.user_bind_groups(user_serv['user_id'], user_group_list)

        if user_role_list:
            RoleService.bind_user_role(user_serv['user_id'], user_role_list)
        return user_serv, None

    @staticmethod
    def group_user_edit(params):  # 更名或者单独起一个文件 方法这个方法
        # 用户角色部门绑定
        user_role_list = params.get('user_role_list', None)
        user_group_list = params.get('user_group_list', None)
        user_id = params.get("user_id")
        if not user_id:
            return None, "msg:用户ID错误;tip:非法请求"
        if not user_group_list is None:
            data, err = UserGroupService.user_bind_groups(params.get("user_id"), user_group_list)
            if err:
                return None, "msg:" + str(err).replace(":", " ") + ";tip:部门修改异常"

        if not user_role_list is None:
            data, err = RoleService.bind_user_roles(params.get("user_id"), user_role_list)
            if err:
                return None, "msg:" + str(err).replace(":", " ") + ";tip:角色修改异常"

        # 联动修改用户详情
        data, err = UserService.user_edit(
            params={
                "user_id": params.get("user_id"),
                "real_name": params.get("real_name"),
                "is_using": params.get("is_using"),
            },user_id = params.get("user_id")
        )
        if err:
            return None, "联动用户详情修改异常：" + err
        return None, None
    # ===============  用户分组和角色关系操作服务 start ===============


    # #根据用户查分组列表
    # @staticmethod
    # def user_group_list(params: dict = None):
    #     user_group = db.table(db.raw(f"role_user_to_group as rr")).left_join(db.raw(f"user_base_info as u"),
    #                                                                               'rr.user_id',
    #                                                                               '=', 'u.id').left_join(db.raw(f"role_user_group as g"),
    #                                                                               'rr.user_group_id',
    #                                                                               '=', 'g.id').where("rr.user_id",9).get()
    #     results_list = user_group.items
    #     return results_list, None
