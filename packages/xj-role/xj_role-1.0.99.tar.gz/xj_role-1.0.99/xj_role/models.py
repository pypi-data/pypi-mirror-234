from django.db import models


class RoleUserGroup(models.Model):
    using_choices = (
        (1, "是"),
        (2, "否")
    )
    """ 3、Role_RoleUserGroup 用户分组表 """
    id = models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, help_text='')
    group = models.CharField(verbose_name='用户组', max_length=32, blank=True, null=True, help_text='')
    group_name = models.CharField(verbose_name='用户组名', max_length=32, blank=True, null=True, help_text='')
    parent_group = models.ForeignKey(verbose_name='父组ID', to="self", unique=False, blank=True, null=True,
                                     on_delete=models.DO_NOTHING)
    sort = models.IntegerField(verbose_name='排序', blank=True, null=True, help_text='', )
    is_using = models.IntegerField(verbose_name='是否使用', default=1, choices=using_choices, blank=True, null=True,
                                   help_text='')
    description = models.CharField(verbose_name='描述', max_length=32, blank=True, null=True, help_text='')
    manager_name = models.CharField(verbose_name='负责人', max_length=32, blank=True, null=True, help_text='')
    manager_phone = models.CharField(verbose_name='联系电话', max_length=32, blank=True, null=True, help_text='')

    class Meta:
        db_table = 'role_user_group'
        verbose_name_plural = "03. 角色 - 用户分组表"

    def __str__(self):
        return f"{self.group}"


class Role(models.Model):
    """ 1、Role_Role 主表 [NF1]"""
    id = models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, help_text='')
    role = models.CharField(verbose_name='角色', max_length=32, blank=True, null=True, help_text='')
    role_name = models.CharField(verbose_name='角色名称', max_length=32, blank=True, null=True, help_text='')
    parent_role_id = models.IntegerField(verbose_name='父级角色ID', blank=True, null=True, help_text='')
    user_group = models.ForeignKey(RoleUserGroup, verbose_name='分组ID', max_length=32, blank=True, null=True,
                                   help_text='', on_delete=models.DO_NOTHING, )
    sort = models.IntegerField(verbose_name='排序', blank=True, null=True, help_text='', )
    is_delete = models.IntegerField(verbose_name='是否删除', blank=True, null=True, default=0, help_text='')
    is_using = models.IntegerField(verbose_name='是否使用', blank=True, null=True, default=1, help_text='')
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, blank=True, null=True)
    description = models.CharField(verbose_name='描述', max_length=32, blank=True, null=True, help_text='')

    class Meta:
        db_table = 'role_role'
        verbose_name_plural = "01. 角色 - 角色列表"

    def __str__(self):
        return f"{self.role_name}"


class UserToGroup(models.Model):
    """  4、Role_UserToGroup 多对多用户分组表[N-N]** """
    id = models.IntegerField(verbose_name='ID', primary_key=True, auto_created=True, help_text='')
    user_id = models.IntegerField(verbose_name='用户ID', blank=True, null=True, help_text='')
    user_group = models.ForeignKey(RoleUserGroup, verbose_name='分组ID', blank=True, null=True,
                                   on_delete=models.DO_NOTHING, help_text='')

    class Meta:
        db_table = 'role_user_to_group'
        verbose_name_plural = "04. 角色 - 多对多用户分组表"

    def __str__(self):
        return f"{self.user_group}"


class UserToRole(models.Model):
    """  2、Role_UserToRole 多对多用户角色表[N-N] """
    id = models.IntegerField(verbose_name='ID', primary_key=True, auto_created=True, help_text='')
    user_id = models.IntegerField(verbose_name='用户ID', blank=True, null=True, help_text='')
    role = models.ForeignKey(Role, verbose_name='角色ID', blank=True, null=True, on_delete=models.DO_NOTHING,
                             help_text='')

    class Meta:
        db_table = 'role_user_to_role'
        verbose_name_plural = "02. 角色 - 多对多用户角色表"

    def __str__(self):
        return f"{self.role}"


class RoleApi(models.Model):
    """  2、Role_UserToRole 多对多用户角色表[N-N] """
    using_choices = (
        (1, "是"),
        (2, "否")
    )
    method_choices = (
        ("POST", "POST"),
        ("GET", "GET"),
        ("PUT", "PUT"),
        ("DELETE", "DELETE"),
        ("PATCH", "PATCH"),
        ("COPY", "COPY"),
        ("OPTIONS", "OPTIONS"),
        ("LINK", "LINK"),
        ("LOCK", "LOCK"),
        ("VIEW", "VIEW")
    )
    id = models.IntegerField(verbose_name='ID', primary_key=True, auto_created=True, help_text='')
    module = models.CharField(verbose_name="模型", max_length=50, blank=True, null=True, )
    route = models.CharField(verbose_name='路由', max_length=500, blank=True, null=True, help_text='')
    method = models.CharField(verbose_name='请求类型', max_length=15, choices=method_choices, blank=True, null=True,
                              help_text='')
    name = models.CharField(verbose_name='路由名称', max_length=500, blank=True, null=True, help_text='')
    is_using = models.IntegerField(verbose_name='是否使用', default=1, choices=using_choices, blank=True, null=True,
                                   help_text='')
    is_delete = models.IntegerField(verbose_name='是否删除', default=0, choices=using_choices, blank=True, null=True,
                                    help_text='')
    is_open_api = models.IntegerField(verbose_name='开放接口', default=1, choices=using_choices, blank=True, null=True,
                                      help_text='是否是开发API，该API在没有登录的情况可直接访问。')
    description = models.CharField(verbose_name='API使用介绍', max_length=5000, default="", blank=True, null=True,
                                   help_text='')
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, blank=True, null=True, help_text='')
    update_time = models.DateTimeField(verbose_name='创建时间', auto_now=True, blank=True, null=True, help_text='')

    class Meta:
        db_table = 'role_api'
        verbose_name_plural = "角色 - 角色API表"

    def __str__(self):
        return f"{self.name}"


class RoleMenu(models.Model):
    class Meta:
        db_table = 'role_menu'
        verbose_name_plural = "角色 - 系统菜单表"

    bool_choices = (
        (1, "是"),
        (0, "否")
    )
    level_choices = (
        (1, "目录"),
        (2, "菜单"),
        (3, "操作")
    )

    id = models.IntegerField(verbose_name='ID', primary_key=True, auto_created=True, help_text='')
    category_id = models.IntegerField(verbose_name='类别ID', blank=True, null=True, help_text='')
    parent_id = models.IntegerField(verbose_name='父级ID', default=0, help_text='')
    name = models.CharField(verbose_name='菜单名', max_length=120, blank=True, null=True, help_text='')
    route = models.CharField(verbose_name='页面路由', max_length=120, blank=True, null=True, help_text='')
    icon = models.CharField(verbose_name='菜单图标', max_length=1000, blank=True, null=True, help_text='')
    link = models.CharField(verbose_name='外部链接', max_length=1000, blank=True, null=True, help_text='')
    level = models.IntegerField(verbose_name='菜单层级', default=1, choices=level_choices, blank=True, help_text='')
    config = models.JSONField(verbose_name='菜单配置', blank=True, null=True, help_text='')
    description = models.CharField(verbose_name='路由使用介绍', max_length=1000, blank=True, null=True, help_text='')
    is_using = models.IntegerField(verbose_name='是否启用', default=1, choices=bool_choices, blank=True, null=True,
                                   help_text='')
    is_delete = models.IntegerField(verbose_name='是否删除', default=0, choices=bool_choices, blank=True, null=True,
                                    help_text='')
    is_jump_link = models.IntegerField(verbose_name='链接菜单', default=0, choices=bool_choices, blank=True, null=True,
                                       help_text='是否为跳转链接菜单')
    sort = models.IntegerField(verbose_name='排序', blank=True, null=True, help_text='')
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, blank=True, null=True, help_text='')
    updated_time = models.DateTimeField(verbose_name='更新时间', auto_now=True, blank=True, null=True, help_text='')

    def __str__(self):
        return f"{self.name}"


class RolePermission(models.Model):
    type_choices = [
        ('API', '接口权限'), ('MENU', '菜单权限'), ('DATA', '数据类别权限')
    ]
    data_set_type_choices = [
        ('THREAD', '信息模块'), ('FINANCE', '资金模块'), ("USER", "用户模块")
    ]

    id = models.AutoField(verbose_name='ID', primary_key=True)
    type = models.CharField(verbose_name='权限ID', max_length=20, choices=type_choices, help_text='')
    role = models.ForeignKey(to=Role, verbose_name='角色ID', blank=True, null=True, on_delete=models.DO_NOTHING)
    api = models.ForeignKey(to=RoleApi, verbose_name="接口ID", blank=True, null=True, on_delete=models.DO_NOTHING)
    menu = models.ForeignKey(to=RoleMenu, verbose_name="接口ID", blank=True, null=True, on_delete=models.DO_NOTHING)
    data_set_id = models.IntegerField(verbose_name="数据集ID", blank=True, null=True)
    data_set_type = models.CharField(verbose_name="数据集类型", max_length=50, choices=data_set_type_choices,
                                     blank=True, null=True)
    filter_filed_list = models.JSONField(verbose_name="过滤字段", blank=True, null=True, default=[])
    remove_filed_list = models.JSONField(verbose_name="移除字段", blank=True, null=True, default=[])
    default_value_dict = models.JSONField(verbose_name="默认值", blank=True, null=True, default={})
    allow_values_dict = models.JSONField(verbose_name="允许传递值", blank=True, null=True, default={})
    output_filter_filed_list = models.JSONField(verbose_name="输出过滤字段列表", blank=True, null=True, default=[])
    output_remove_filed_list = models.JSONField(verbose_name="输出移除字段列表", blank=True, null=True, default=[])
    description = models.CharField(verbose_name="描述", max_length=500, default="")
    created_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    class Meta:
        db_table = 'role_permission_v2'
        verbose_name_plural = "06. 角色 - 权限组值表"
        ordering = ['id']

    def __str__(self):
        return f"{self.type}-{self.id}"
