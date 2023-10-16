# encoding: utf-8
"""
@project: djangoModel->role_service
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 角色服务
@created_time: 2022/9/2 15:37
"""
from django.core.paginator import Paginator, EmptyPage
from django.db import transaction
from django.db.models import F

from xj_user.services.user_detail_info_service import DetailInfoService
from ..models import Role, UserToRole
from ..utils.custom_tool import format_list_handle, force_transform_type, filter_fields_handler
from ..utils.custom_tool import format_params_handle, filter_result_field
from ..utils.j_recur import JRecur
from ..utils.join_list import JoinList


# 用户组 树状数据返回
class RoleTreeService(object):
    @staticmethod
    def role_tree(role_id=0, role_key=None, params=None):
        """
        角色树
        :param role_id: 角色ID
        :param role_key: 居色Key
        :param params: 搜索参数
        """
        params, err = force_transform_type(variable=params, var_type="only_dict", default={})
        filter_tree_params, err = JRecur.get_filter_tree_params(params=params)

        data_list = list(Role.objects.all().values())
        role_tree = JRecur.create_forest(data_list, primary_key="id", parent_key="parent_role_id", children_key='children')
        if role_id:
            role_tree = JRecur.filter_forest(role_tree, find_key="id", find_value=role_id, children_key='children')
        elif role_key:
            role_tree = JRecur.filter_forest(role_tree, find_key="role", find_value=role_key, children_key='children')
        elif filter_tree_params:
            for k, v in filter_tree_params.items():
                if not v:
                    continue
                role_tree = JRecur.filter_forest(role_tree, find_key=k, find_value=v, children_key='children')

        return role_tree, None


class RoleService:
    role_all_fields = [i.name for i in Role._meta.fields] + ["user_group_id"]

    # ============= section 角色基础服务 =============
    @staticmethod
    def add_role(params):
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=["role", "role_name", "parent_role_id|int", "user_group_id|int", "is_using|int", "sort|int", "description"]
        )

        if not params:
            return None, "参数不能为空"
        try:
            instance = Role.objects.create(**params)
            return {"id": instance.id}, None
        except Exception as e:
            return None, "msg:" + str(e).replace(":", " ").replace(";", " ") + ";tip:添加错误"

    @staticmethod
    def edit_role(params: dict = None):
        params, is_pass = force_transform_type(variable=params, var_type="dict", default={})
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=[
                "id|int", "role_id|int", "role", "role_key", "role_name", "parent_role_id|int", "user_group_id|int", "is_using|int", "is_delete|int", "description"
                , "sort|int"
            ],
            alias_dict={"id": "role_id", "name": "role_name", "role_key": "role"}
        )
        role_id = params.pop("role_id", params.get("id"))
        if not role_id:
            return None, "ID 不可以为空"
        if not params:
            return None, "没有可以修改的字段"
        instance = Role.objects.filter(id=role_id)
        instance.update(**params)
        return None, None

    @staticmethod
    def del_role(id):
        if not id:
            return None, "ID 不可以为空"

        # user_role_set = UserToRole.objects.filter(role_id=id).exists()
        # if user_role_set:
        #     return None, "该角色有绑定关系,无法删除"
        instance = Role.objects.filter(id=id).first()
        if instance:
            Role.objects.filter(id=id).update(is_delete=1)
        return None, None

    @staticmethod
    def get_role_list(params: dict = None, need_pagination: bool = True, only_first: bool = False, get_tree=False, filter_fields: "str|list" = None, **kwargs):
        """
        查询角色列表,
        @note 强烈建议把下面的接口全部合并到该服务中
        :param get_tree: 是否查询树结构数据
        :param only_first: 是否仅仅查看第一条
        :param filter_fields: 过滤字段
        :param params: 查询参数
        :param need_pagination: 是否需要分页
        :return: data, err
        """
        # =========== section 参数处理 start ====================
        kwargs, is_pass = force_transform_type(variable=kwargs, var_type="dict", default={})
        params, is_pass = force_transform_type(variable=params, var_type="dict", default={})
        params.update(kwargs)
        need_pagination, is_pass = force_transform_type(variable=need_pagination, var_type="bool", default=True)
        only_first, is_pass = force_transform_type(variable=only_first, var_type="bool", default=False)
        get_tree, is_pass = force_transform_type(variable=get_tree, var_type="bool", default=False)
        page, is_pass = force_transform_type(variable=params.pop("page", 1), var_type="int", default=1)
        size, is_pass = force_transform_type(variable=params.pop("size", 10), var_type="int", default=10)

        sort = params.pop("sort", "-role_id")
        sort = sort if sort in ["role_id", "-role_id", "sort", "-sort"] else "-role_id"
        filter_tree_params, err = JRecur.get_filter_tree_params(params)
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=[
                "role_id|int", "role", "role_key|str", "user_group_id|int", "parent_role_id|int", "user_id|int", "is_using|int", "is_delete|int",
                "user_group_id_list|list_int", "role_id_list|list_int", "user_id_list|list_int", "role_name|str",
                "created_time_start", "created_time_end"
            ],
            split_list=["user_group_id_list", "role_id_list", "user_id_list"],
            alias_dict={
                "user_group_id_list": "user_group_id__in", "role_id_list": "role_id__in", "role": "role_key", "role_name": "role_name__contains",
                "created_time_start": "created_time__gte", "created_time_end": "created_time__lte",
            }
        )
        params.setdefault("is_delete", 0)
        user_id = params.pop("user_id", None)
        user_id_list = params.pop("user_id_list", None)

        filter_fields = filter_fields_handler(
            input_field_expression=filter_fields,
            all_field_list=RoleService.role_all_fields
        )
        filter_fields = filter_fields + ["role_id", "role_key"]
        # =========== section 参数处理 end   ====================

        # =========== section 构建ORM start ====================
        if user_id or user_id_list:
            role_query_set = UserToRole.objects.extra(
                select={"created_time": 'DATE_FORMAT(role_role.created_time, "%%Y-%%m-%%d %%H:%%i:%%s")'}
            ).annotate(
                role_key=F("role__role"),  # 字敦冲突别名搜索
                role_name=F("role__role_name"),
                parent_role_id=F("role__parent_role_id"),
                user_group=F("role__user_group"),
                user_group_id=F("role__user_group_id"),
                sort=F("role__sort"),
                description=F("role__description"),
                is_delete=F("role__is_delete"),
                is_using=F("role__is_using"),
                created_time=F("role__created_time")
            )
            if user_id:
                role_query_set = role_query_set.filter(user_id=user_id)
            else:
                role_query_set = role_query_set.filter(user_id__in=user_id_list)
            filter_fields.append("user_id")  # 返回用户ID
        else:
            role_query_set = Role.objects.extra(
                select={"created_time": 'DATE_FORMAT(created_time, "%%Y-%%m-%%d %%H:%%i:%%s")'}
            ).annotate(role_id=F("id"), role_key=F("role"), role_created_time=F("created_time")).filter(**params)

        role_query_set = role_query_set.order_by(sort).values(*filter_fields)
        total = role_query_set.count()
        # =========== section 构建ORM end   ====================

        # =========== section 数据分页 start ====================
        if only_first:
            return role_query_set.first(), None

        # 查询树形数据
        if get_tree:
            role_tree = JRecur.create_forest(
                list(role_query_set),
                primary_key="id",
                parent_key="parent_role_id",
                children_key="children"
            )
            if filter_tree_params:
                for k, v in filter_tree_params.items():
                    role_tree = JRecur.filter_forest(
                        source_forest=role_tree,
                        find_key=k,
                        find_value=v,
                    )
            return role_tree, None

        if (not need_pagination and total <= 2000) or (user_id or user_id_list):
            finish_set = list(role_query_set)
        else:
            paginator = Paginator(role_query_set, size)
            try:
                page_query_set = paginator.page(page)
            except EmptyPage:
                page_query_set = paginator.page(paginator.num_pages)
            finish_set = list(page_query_set.object_list)
        # =========== section 数据分页 end   ====================

        # =========== section 参数自定义序列化 start ===========
        finish_set = filter_result_field(
            result_list=finish_set,
            remove_filed_list=["id", "user_group", ],
            alias_dict={"role_key": "role"}
        )
        result = finish_set if (not need_pagination and total <= 2000) or (user_id or user_id_list) else {'size': size, 'page': page, 'total': total, 'list': finish_set}
        # =========== section 参数自定义序列化 end   ===========
        return result, None

    # ============= section 角色基础服务 =============

    # ============= section 角色对用户服务 =============
    # 判断该用户是否属于该角色,提供其他服务直接调用
    @staticmethod
    def is_this_role(user_id=None, role_id=None, role_key=None):
        """
        判断该用户是否属于该角色
        :return: res, err
        """
        if not user_id or (not role_id and not role_key):
            return False, None
        role_obj = UserToRole.objects.annotate(role_key=F("role__role")).filter(user_id=user_id)
        if role_id:
            res = role_obj.filter(role_id=role_id).first()
        else:
            res = role_obj.filter(role_key=role_key).first()
        return True if res else False, None

    # 用户绑定角色
    @staticmethod
    def user_bind_role(user_id, role_id: int = None, role_value: str = None):
        """
        用户绑定角色
        :param user_id: 需要绑定用户的用户ID
        :param role_id: 绑定的角色ID
        :param role_value: 绑定角色Value值
        :return: None, err
        """
        # 如果存在role_value，则有限使用role_value查询添加的角色
        if not role_value is None:
            find_role_id = Role.objects.filter(role=role_value).values("id").first()
            role_id = find_role_id.get("id", None) if find_role_id else role_id

        # 参数校验
        if not user_id or not role_id:
            return None, "参数错误，user_id, role_id 必传"

        # 部门校验
        role_is_set = Role.objects.filter(id=role_id).first()
        if not role_is_set:
            return None, "该角色不存在"

        # 绑定角色
        try:
            find_user_role = UserToRole.objects.filter(user_id=user_id, role_id=role_id).first()
            if find_user_role:
                return None, None
            UserToRole.objects.create(user_id=user_id, role_id=role_id)
            return None, None
        except Exception as e:
            return None, "msg:" + str(e) + ";tip:添加失败，请不要选择有效的角色，不要选择部门。"

    @staticmethod
    def bind_user_roles(user_id: int, role_list):
        """
        批量绑定用户角色信息
        :param user_id:
        :param role_list:
        """
        return RoleService.bind_user_role(user_id=user_id, role_list=role_list)

    # 批量绑定用户角色信息 TODO 改名为 bind_user_roles
    @staticmethod
    def bind_user_role(user_id: int, role_list):
        """
        批量绑定用户角色信息
        :param user_id:
        :param role_list:
        :return:
        """
        if not role_list:
            UserToRole.objects.filter(user_id=user_id).delete()
            # 没有传值则
            return None, None

        role_list = role_list.split(',') if isinstance(role_list, str) else role_list
        if not role_list:
            return None, "至少选择一个角色"

        sid = transaction.savepoint()
        try:
            UserToRole.objects.filter(user_id=user_id).delete()
            for i in role_list:
                data = {
                    "user_id": user_id,
                    "role_id": i
                }
                UserToRole.objects.create(**data)
            transaction.clean_savepoints()
            return None, None
        except Exception as e:
            transaction.savepoint_rollback(sid)
            return None, str(e)

    # 用户绑定角色
    @staticmethod
    def user_remove_role(user_id, role_id: int = None, role_value: str = None):
        """
        用户绑定角色
        :param user_id: 需要绑定用户的用户ID
        :param role_id: 绑定的角色ID
        :param role_value: 绑定角色Value值
        :return: None, err
        """
        # 如果存在role_value，则有限使用role_value查询需要移除的角色
        if not role_value is None:
            find_role_id = Role.objects.filter(role=role_value).values("id").first()
            role_id = find_role_id.get("id", None) if find_role_id else role_id

        # 参数校验
        if not user_id or not role_id:
            return None, "参数错误，user_id, role_id 必传"

        # 移除用户绑定的角色
        try:
            find_user_role = UserToRole.objects.filter(user_id=user_id, role_id=role_id).first()
            if not find_user_role:
                return None, None
            UserToRole.objects.filter(user_id=user_id, role_id=role_id).delete()
            return None, None
        except Exception as e:
            return None, "msg:" + str(e) + ";tip:移除失败，请不要选择有效的角色，不要选择部门。"

    # 查询居角色于用户的绑定关系列表
    @staticmethod
    def user_role_users(params: dict = None, is_subtree: bool = False, without_user_info: bool = False, **kwargs):
        """
        查询居角色于用户的绑定关系列表
        :param params:  搜索参数
        :param without_user_info: 返回结果不携带用户信息。 服务层调用不需要过多信息，使用该参数。
        :param is_subtree: 是否查询子角色的所有用户
        :return: data ,err
        """
        params, is_pass = force_transform_type(variable=params, var_type="dict", default={})
        without_user_info, is_pass = force_transform_type(variable=without_user_info, var_type="bool", default=False)

        page, is_pass = force_transform_type(variable=params.pop("page", kwargs.pop("page", 1)), var_type="int", default=1)
        size, is_pass = force_transform_type(variable=params.pop("size", kwargs.pop("size", 10)), var_type="int", default=10)

        user_id, is_pass = force_transform_type(variable=params.pop("user_id", kwargs.pop("user_id", None)), var_type="int")
        user_id_list, is_pass = force_transform_type(variable=params.pop("user_id_list", kwargs.pop("user_id_list", None)), var_type="list_int")

        role_id, is_pass = force_transform_type(variable=params.pop("role_id", kwargs.pop("role_id", None)), var_type="int")
        role_key = params.pop("role_key", kwargs.pop("role_key", None))
        is_subtree, is_pass = force_transform_type(variable=is_subtree, var_type="bool", default=False)
        # ==== section 用户详细信息反查 start ====
        user_search_params = format_params_handle(
            param_dict=params,
            filter_filed_list=["user_name", "full_name", "nickname", "phone", "email", "real_name"]
        )
        if user_search_params:
            user_search_params["size"] = 200
            user_id_list, err = DetailInfoService.get_list_detail(params=user_search_params, filter_fields=["user_id"])
            user_id_list = [i["user_id"] for i in user_id_list.get("list", [])]
        # ==== section 用户详细信息反查 end   ====

        # ===== section 构建ORM查询角色相关信息 start ====
        user_to_role_query = UserToRole.objects.annotate(role_name=F("role__role_name"), role_key=F("role__role")).values("user_id", "role_id", "role_name", "role_key")
        # 角色搜索
        if is_subtree:
            role_id_tree, err = RoleTreeService.role_tree(role_id=role_id, role_key=role_key)
            if err:
                return None, err
            role_id_list = JRecur.get_value_in_forest(role_id_tree, field="id")
            user_to_role_query = user_to_role_query.filter(role__in=role_id_list)
        else:
            if role_id:
                user_to_role_query = user_to_role_query.filter(role=role_id)
            if role_key:
                user_to_role_query = user_to_role_query.filter(role_key=role_key)
        # 用户相关搜索
        if user_id_list:
            user_to_role_query = user_to_role_query.filter(user_id__in=user_id_list)
        if user_id:
            user_to_role_query = user_to_role_query.filter(user_id=user_id)
        # 如果不需要用户信息直接返回角色ID列表
        if without_user_info:
            return list(user_to_role_query), None

        # 分页查询
        total = user_to_role_query.count()
        paginator = Paginator(user_to_role_query, size)
        try:
            paginator = paginator.page(page)
        except EmptyPage:
            paginator = paginator.page(paginator.num_pages)
        user_role_list = list(paginator.object_list)
        # ===== section 构建ORM查询角色相关信息 end   ====

        user_id_list = [it['user_id'] for it in user_role_list]
        if not user_id_list:
            return {"total": 0, "page": page, "size": size, "list": []}, None
        # 数据拼接
        user_detail_list, err = DetailInfoService.get_list_detail(user_id_list=user_id_list, )
        user_role_list = JoinList(l_list=user_role_list, r_list=user_detail_list, l_key="user_id", r_key="user_id").join()
        return {"total": total, "page": page, "size": size, "list": user_role_list}, None

    # ============= section 角色对用户服务 =============

    # ============= note 即将弃用方法 =============
    # 按角色ID获取相关用户列表
    # TODO user_list_by_roles即将删除，使用 user_role_users 代替。维护一个服务即可。
    @staticmethod
    def user_list_by_roles(role_list):
        """按角色ID获取相关用户列表"""
        return list(UserToRole.objects.filter(role_id__in=role_list).values() or [])

    # TODO get_user_role_info即将删除，使用get_role_list代替。维护一个服务即可。
    @staticmethod
    def get_user_role_info(user_id: int = None, user_id_list: list = None, field_list=None, **kwargs):
        """
        获取用户的角色信息
        :param user_id: 用户id
        :param user_id_list: 用户的ID列表
        :param field_list: 字段过滤列表
        :return: 用户的角色列表，err
        """
        # 找不到可检索的用户，则直接返回，可以使用单个ID检索也可以使用ID列表检索。
        if not user_id and not user_id_list:
            return [], None

        # 过滤字段合法性验证
        allow_field_list = ["user_id", 'role_id', 'role_name', 'role_value', 'description']
        field_list = format_list_handle(
            param_list=field_list or [],
            filter_filed_list=allow_field_list
        )
        field_list = allow_field_list if not field_list else field_list
        # query 对象
        user_role_obj = UserToRole.objects.annotate(
            role_name=F("role__role_name"),
            role_value=F("role__role"),
            description=F("role__description"),
        ).values(*field_list)
        # 分情况检索数据
        if user_id:
            user_role_list = user_role_obj.filter(user_id=user_id)
            return list(user_role_list), None  # 返回用户的部门（分组）列表
        else:
            user_role_list = UserToRole.objects.filter(user_id__in=user_id_list)
            user_role_map = {}  # 按照用户进行映射
            for item in list(user_role_list):
                if user_role_map.get(item['user_id']):
                    user_role_map[item['user_id']].append(item)
                else:
                    user_role_map[item['user_id']] = [item]
            return user_role_map, None  # 返回映射字典

    # TODO get_user_role_info即将删除，使用get_role_list或者 user_role_users a代替。维护一个服务即可。
    @staticmethod
    def user_role_list(user_id):
        """获取当前用户的所有角色"""
        return list(UserToRole.objects.filter(user_id=user_id).annotate(
            role_value=F('role_id__role'),
            role_name=F('role_id__role_name'),
            user_group_value=F('role_id__user_group__group'),
            user_group_name=F('role_id__user_group__group_name'),
        ).values('id', 'role_id', 'user_id', 'role_value', 'role_name', 'user_group_value', 'user_group_name'))

    # TODO 即将删除 使用 RoleTreeService.role_tree 方法代替
    @staticmethod
    def get_user_role_tree(role_id=None, is_family_tree=False):
        """
        获取用户所在角色树
        @param group_id 用户组ID，如果有则过滤用户组，没有会返回全部分组，请慎用。
        @param is_family_tree 是否返回整个家族数。
        """
        data_list = list(Role.objects.filter().annotate(name=F('role_name')).values(
            "id",
            "role",
            "role_name",
            "parent_role_id",
            "user_group_id",
            "description",
        ))
        role_tree = JRecur.create_forest(data_list, parent_key='parent_role_id')
        if role_id:
            role_tree = JRecur.filter_forest(
                source_forest=role_tree,
                find_key='id',
                find_value=role_id,
                is_family_tree=is_family_tree
            )
        return role_tree, None

    # ============= note 即将弃用方法 =============
