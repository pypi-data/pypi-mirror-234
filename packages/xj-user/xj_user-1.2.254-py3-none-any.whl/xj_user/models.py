import uuid

from django.db import models
from django.utils import timezone

prefix = ''  # 'bx' + '_'

user_identity_choices = (
    (1, '普通用户'),
    (2, '镖师'),
    (3, '业务员'),
)

using_choices = (
    (1, "是"),
    (2, "否")
)

class BaseInfo(models.Model):
    """ 1、User_Base_Info 基础信息表 [NF1] """
    id = models.AutoField(verbose_name='ID', primary_key=True)
    uuid = models.UUIDField(verbose_name='UUID', default=uuid.uuid4, unique=True, editable=True, blank=True, null=True)
    user_no = models.CharField(verbose_name='用户编号', max_length=32, unique=True, db_index=True, blank=True, null=True)
    user_name = models.CharField(verbose_name='用户名', max_length=32, unique=True, blank=True, null=True, db_index=True,
                                 help_text='登录的用户名')
    nickname = models.CharField(verbose_name='昵称', max_length=128, blank=True, null=True, help_text='')
    full_name = models.CharField(verbose_name='姓名', max_length=128, blank=True, null=True, db_index=True,
                                 help_text='用户的姓名（未实名验证）')
    phone = models.CharField(verbose_name='手机', max_length=128, unique=False, blank=True, null=True, db_index=True,
                             help_text='登录用的手机号')
    email = models.EmailField(verbose_name='邮箱', unique=False, blank=True, null=True, db_index=True, help_text='登录用的邮箱')
    user_type = models.CharField(verbose_name='用户类型', max_length=255, blank=True, null=True,
                                 choices=[('PERSON', '个人用户'), ('COMPANY', '企业用户'), ('ADMIN', '管理员用户')],
                                 help_text='PERSON 个人用户, COMPANY 企业用户')
    user_info = models.JSONField(verbose_name='用户信息', blank=True, null=True, help_text='用户扩展信息')
    privacies = models.JSONField(verbose_name='用户隐私设置', blank=True, null=True, help_text='用户隐私设置')
    register_ip = models.GenericIPAddressField(verbose_name='注册IP', protocol='both', blank=True, null=True,
                                               help_text='')
    register_time = models.DateTimeField(verbose_name='注册时间', default=timezone.now, blank=True, null=True, help_text='')
    platforms_to_users = models.ManyToManyField(to='Platform', through="PlatformsToUsers",
                                                through_fields=("user", "platform"))
    is_delete = models.BooleanField(verbose_name='是否删除', default=False, blank=True, null=True, )
    user_identity = models.IntegerField(verbose_name='用户身份', default=1, blank=True, null=False, choices=user_identity_choices)
    is_using = models.IntegerField(verbose_name='是否使用', default=1, choices=using_choices, blank=True, null=True,
                                   help_text='')

    class Meta:
        db_table = prefix + 'user_base_info'
        # unique_together = [['platform', 'platform_uid'], ['platform', 'user_name']]
        verbose_name_plural = "01. 用户 - 基础信息"
        ordering = ["-register_time"]

    def __str__(self):
        # return f"{self.user_name}({self.full_name})"
        return f"{self.full_name} ({self.user_name})"

    def user_info_short(self):
        if len(str(self.user_info)) > 30:
            return '{}...'.format(str(self.user_info)[0:30])
        return self.user_info

    user_info_short.short_description = '用户信息'

    def privacies_short(self):
        if len(str(self.privacies)) > 30:
            return '{}...'.format(str(self.privacies)[0:30])
        return self.privacies

    privacies_short.short_description = '用户隐私设置'

    def uuid_short(self):
        return '{}'.format(str(self.uuid)[0:8])

    uuid_short.short_description = 'UUID'


id_card_type_choices = (
    ('IDENTITY', '身份证'),
    ('PASSPORT', '护照'),
    ('DRIVING', '驾驶证'),
    ('BUSINESS', '营业执照'),
)

language_choices = (
    ('cn', '简体中文'),
    ('en', 'English'),
    ('ru', 'Русский'),
    ('tc', '繁体中文'),
    ('fr', 'Français'),
    ('de', 'Deutsch'),
    ('jp', '日本語'),
)


class DetailInfo(models.Model):
    sex_choices = [("0", "未知"), ("1", "男"), ("2", "女"), ]
    """ 2、User_Detail_Info 详细信息表 [1-1] """
    user = models.OneToOneField(BaseInfo, verbose_name='用户', unique=True, db_column="user_id", db_constraint=False,
                                on_delete=models.DO_NOTHING, help_text='登录用的用户名')
    # user_uuid = models.UUIDField(verbose_name='用户UUID', default=uuid.uuid4, unique=True, blank=True, null=True)  # 对同一数据库内并不需要这个字段，所以外键是有ID就够了 20230822 by Sieyoo
    real_name = models.CharField(verbose_name='实名姓名', max_length=50, blank=True, null=True, db_index=True,
                                 help_text='实名认证后的真名')
    sex = models.CharField(verbose_name='性别', max_length=1, blank=True, null=True, help_text='0未知 1男 2女',
                           choices=sex_choices)
    birth = models.DateField(verbose_name='生日', blank=True, null=True, help_text='')
    tags = models.CharField(verbose_name='个人标签', max_length=255, blank=True, null=True,
                            help_text='多个标签以英文;号为分隔符')
    signature = models.CharField(verbose_name='个性签名', max_length=255, blank=True, null=True, help_text='')
    avatar = models.CharField(verbose_name='个人头像', max_length=2000, blank=True, null=True, help_text='')
    cover = models.CharField(verbose_name='个人主页封面', max_length=2000, blank=True, null=True, help_text='')
    id_card_type = models.CharField(verbose_name='证件类型', max_length=32, blank=True, null=True,
                                    choices=id_card_type_choices, help_text='用于实名认证姓名时的证件类型')
    id_card_no = models.CharField(verbose_name='证件号码', max_length=32, blank=True, null=True, help_text='')
    language = models.CharField(verbose_name='我使用的语言', max_length=32, blank=True, null=True, choices=language_choices,
                                help_text='')
    region_code = models.BigIntegerField(verbose_name='所在地行政区划编码', blank=True, null=True, help_text='')
    subcompany = models.OneToOneField('UserSubCompany', verbose_name='分子公司', unique=True, db_column="subcompany_id",
                                      db_constraint=False,
                                      on_delete=models.DO_NOTHING, help_text='分子公司ID')
    more = models.JSONField(verbose_name='更多信息', blank=True, null=True,
                            help_text='更多信息用来存放用户可能填写的扩展内容，由于很多信息不是必填或必须存在的，因此不单独建字段。')
    field_1 = models.CharField(verbose_name='字段1', max_length=255, blank=True, null=True, help_text='')
    field_2 = models.CharField(verbose_name='字段2', max_length=255, blank=True, null=True, help_text='')
    field_3 = models.CharField(verbose_name='字段3', max_length=255, blank=True, null=True, help_text='')
    field_4 = models.CharField(verbose_name='字段4', max_length=255, blank=True, null=True, help_text='')
    field_5 = models.CharField(verbose_name='字段5', max_length=255, blank=True, null=True, help_text='')
    field_6 = models.CharField(verbose_name='字段6', max_length=255, blank=True, null=True, help_text='')
    field_7 = models.CharField(verbose_name='字段7', max_length=255, blank=True, null=True, help_text='')
    field_8 = models.CharField(verbose_name='字段8', max_length=255, blank=True, null=True, help_text='')
    field_9 = models.CharField(verbose_name='字段9', max_length=255, blank=True, null=True, help_text='')
    field_10 = models.CharField(verbose_name='字段10', max_length=255, blank=True, null=True, help_text='')
    field_11 = models.TextField(verbose_name='字段11', blank=True, null=True, help_text='')
    field_12 = models.TextField(verbose_name='字段12', blank=True, null=True, help_text='')
    field_13 = models.TextField(verbose_name='字段13', blank=True, null=True, help_text='')
    field_14 = models.TextField(verbose_name='字段14', blank=True, null=True, help_text='')
    field_15 = models.TextField(verbose_name='字段15', blank=True, null=True, help_text='')

    class Meta:
        db_table = prefix + 'user_detail_info'
        verbose_name_plural = "02. 用户 - 详细信息"

    def __str__(self):
        # return f"{self.user_name}({self.real_name})"
        return f"{self.user.user_name}"

    # def user_uuid_short(self):
    #     return '{}'.format(str(self.user_uuid)[0:8])
    # user_uuid_short.short_description = '用户UUID'


class Auth(models.Model):
    """ 3、User_Auth 安全认证表 [1-1] """
    platform = models.ForeignKey(to='Platform', verbose_name='平台', blank=True, null=True, db_constraint=False,
                                 on_delete=models.DO_NOTHING)
    user = models.ForeignKey(BaseInfo, verbose_name='用户', db_constraint=False, on_delete=models.DO_NOTHING)
    # user_uuid = models.UUIDField(verbose_name='用户UUID', default=uuid.uuid4, unique=True, editable=True, blank=True, null=True)
    password = models.CharField(verbose_name='密码', max_length=255, blank=True, null=True, help_text='登录的密码')
    plaintext = models.CharField(verbose_name='PT', max_length=255, blank=True, null=True, help_text='')
    salt = models.CharField(verbose_name='盐', max_length=32, blank=True, null=True,
                            help_text='加密盐由六位数字和字母组成，区分大小写')
    algorithm = models.CharField(verbose_name='加密算法', max_length=255, blank=True, null=True,
                                 choices=[('DEFAULT', 'Default'), ('DISCUZ', 'Discuz (md5(md5(pwd).salt)'),
                                          ('SPSS', 'Spss (sha1(rsa(cip).salt))')],
                                 help_text='系统同时支持多种加密算法，旧版为MD5，新版为SHA1')
    token = models.CharField(verbose_name='临时令牌', max_length=255, blank=True, null=True,
                             help_text='用户令牌，用于验证用户有效期')
    ticket = models.CharField(verbose_name='临时票据', max_length=255, blank=True, null=True,
                              help_text='用户提供第三方单点登录的票据')
    last_update_ip = models.GenericIPAddressField(verbose_name='最后登录网络地址', protocol='both', blank=True, null=True)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, help_text='')
    update_time = models.DateTimeField(verbose_name='最后登录时间', auto_now=True, blank=True, null=True, help_text='')

    class Meta:
        db_table = prefix + 'user_auth'
        verbose_name_plural = "03. 用户 - 安全认证"

    def __str__(self):
        return f"{self.user.user_name}"

    # def user_uuid_short(self):
    #     return '{}'.format(str(self.user_uuid)[0:8])
    # user_uuid_short.short_description = '用户UUID'

    def token_short(self):
        return '{}...{}({})'.format(str(self.token)[0:4], str(self.token)[-5:-1],
                                    len(self.token)) if self.token else self.token

    token_short.short_description = '临时票据'

    def ticket_short(self):
        return '{}...{}({})'.format(str(self.ticket)[0:4], str(self.ticket)[-5:-1],
                                    len(self.ticket)) if self.ticket else self.ticket

    ticket_short.short_description = '临时票据'


# 扩展字段的下拉选项
type_choices = (
    ('image', '图片-image'),
    ('text', '输入框-text'),
    ('plain', '禁止编辑-plain'),
    ('number', '数字类型-number'),
    ('time', ' 时间类型-time'),
    ('select', '选择框-select'),
    ('upload', '上传类型-upload'),
    ('textarea', '文本域-textarea'),
    ('password', '密码-password'),
    ('switch', '开关-switch'),
    ('radio', '视频-radio'),
    ('checkBox', '多选-checkBox'),
    ('date', '日期-date'),
    ('month', '月份-month'),
    ('year', '年-year'),
    ('cascader', '多选-cascader'),
    ('slot', '插槽-slot'),
    ('editor', '富文本-editor')
)

field_index_choices = (
    ('field_1', '自定义字段1'),
    ('field_2', '自定义字段2'),
    ('field_3', '自定义字段3'),
    ('field_4', '自定义字段4'),
    ('field_5', '自定义字段5'),
    ('field_6', '自定义字段6'),
    ('field_7', '自定义字段7'),
    ('field_8', '自定义字段8'),
    ('field_9', '自定义字段9'),
    ('field_10', '自定义字段10'),
    ('field_11', '自定义字段11'),
    ('field_12', '自定义字段12'),
    ('field_13', '自定义字段13'),
    ('field_14', '自定义字段14'),
    ('field_15', '自定义字段15'),
)


class ExtendField(models.Model):
    """ 4、User_Extend_Field 扩展字段表 [1-1] """
    field_index = models.CharField(verbose_name='映射索引名', max_length=255, unique=True, blank=True, null=True,
                                   choices=field_index_choices, help_text='映射到扩展数据表的字段名，如：field_x')
    field = models.CharField(verbose_name='自定义字段', max_length=30, unique=True, blank=True, null=True,
                             help_text='当已有字段不能满足的时候的扩展字段')
    label = models.CharField(verbose_name='标签', max_length=30, unique=True, blank=True, null=True,
                             help_text='自定义字段的标签，用于前端显示')
    type = models.CharField(verbose_name='类型', max_length=255, blank=True, null=True, choices=type_choices,
                            help_text='自定义字段的数据类型，必须和前端相匹配')
    unit = models.CharField(verbose_name='单位', max_length=32, blank=True, null=True,
                            help_text='自定义字段的显示单位，空值表示不需要配置单位')
    default = models.CharField(verbose_name='默认值', max_length=255, blank=True, null=True,
                               help_text='自定义字段的默认值，当前端用户不配置字段值时，使用该默认值')
    config = models.JSONField(verbose_name='配置', blank=True, null=True, help_text='用于前端自由配置一些属性，如选择列表')
    sort = models.IntegerField(verbose_name='排序', blank=True, null=True, help_text='')
    description = models.CharField(verbose_name='字段描述', max_length=255, blank=True, null=True, help_text='')

    class Meta:
        db_table = prefix + 'user_extend_field'
        verbose_name_plural = "04. 用户 - 扩展字段"

    def __str__(self):
        return f"{self.field}"


class AccessLog(models.Model):
    """ 5、*User_Access_Log 访问日志表 [1-N] """
    user = models.ForeignKey(BaseInfo, verbose_name='用户', db_constraint=False, on_delete=models.DO_NOTHING,
                             help_text='用户ID')
    ip = models.CharField(verbose_name='IP', max_length=128, blank=True, null=True, help_text='登录的IP地址')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, help_text='')
    client_info = models.JSONField(verbose_name='客户端信息', blank=True, null=True, help_text='')
    more = models.JSONField(verbose_name='更多信息', max_length=255, blank=True, null=True, help_text='留用')

    class Meta:
        db_table = prefix + 'user_access_log'
        verbose_name_plural = "05. 用户 - 访问日志表"

    def __str__(self):
        # return f"{self.user_name}({self.full_name})"
        return f"{self.user.user_name}"


class History(models.Model):
    """ 6、*User_History 操作历史表 [1-N] """
    user = models.ForeignKey(BaseInfo, verbose_name='用户', db_constraint=False, on_delete=models.DO_NOTHING,
                             help_text='用户ID')
    field = models.CharField(verbose_name='操作字段', max_length=32, blank=True, null=True,
                             help_text='被用户修改的字段')
    old_value = models.CharField(verbose_name='旧值', max_length=255, blank=True, null=True, help_text='修改前的值')
    new_value = models.CharField(verbose_name='新值', max_length=255, blank=True, null=True, help_text='修改后的值')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, help_text='')

    class Meta:
        db_table = prefix + 'user_history'
        verbose_name_plural = "06. 用户 - 操作历史表"

    def __str__(self):
        # return f"{self.user_name}({self.full_name})"
        return f"{self.user.user_name}"


class RestrictRegion(models.Model):
    """ 7、*User_Restrict_Region 限制范围表"""
    user = models.ForeignKey(BaseInfo, verbose_name='用户', db_constraint=False, on_delete=models.DO_NOTHING,
                             help_text='用户ID')
    region_code = models.BigIntegerField(verbose_name='允许的行政区划编码', blank=True, null=True, db_index=True,
                                         help_text='在国内参考 GB/T2260-2002中国行政区划代码，有6位数 9位数 12位数，非中国地区以9开头')

    class Meta:
        db_table = prefix + 'user_restrict_region'
        verbose_name_plural = "07. 用户 - 限制范围表"

    def __str__(self):
        # return f"{self.user_name}({self.full_name})"
        return f"{self.user.user_name}"


class Platform(models.Model):
    """ 8、*User_Platform 平台表 """
    id = models.IntegerField(verbose_name='ID', primary_key=True, help_text='必填。自动生成。')
    platform_id = models.IntegerField(verbose_name='平台ID', primary_key=False, unique=True,
                                      help_text='必填。不自动生成，由运营人员统一设置。')
    platform_code = models.CharField(verbose_name='平台代码', max_length=8, unique=True, help_text='必填。自动生成8为随机编码')
    platform_name = models.CharField(verbose_name='平台名称', max_length=128,
                                     help_text='必填。平台名称可以是中文、英文、俄文等。')

    class Meta:
        db_table = prefix + 'user_platform'
        verbose_name_plural = "07. 用户 - 平台表"

    def __str__(self):
        return f"{self.platform_name}"

    # 以上代码执行的Sql语句
    # CREATE TABLE `user_platform`(`platform_id` integer NOT NULL PRIMARY KEY, `platform_name` varchar(128) NOT NULL);


class PlatformsToUsers(models.Model):
    """ 9、*User_Platforms_To_Users - 多对多平台记录表 [N-N] """
    user = models.OneToOneField(BaseInfo, verbose_name='用户', on_delete=models.DO_NOTHING, db_column='user_id',
                                help_text='', primary_key=True)
    platform = models.ForeignKey(Platform, verbose_name='平台', to_field="platform_id", db_constraint=False,
                                 on_delete=models.DO_NOTHING, help_text='')
    platform_user_id = models.BigIntegerField(verbose_name='平台用户ID', blank=True, null=True, db_index=True,
                                              help_text='')

    class Meta:
        db_table = prefix + 'user_platforms_to_users'
        verbose_name_plural = "09. 用户 - 多对多平台记录表"
        # managed = False   # 是否对数据库表的创建、修改或删除操作

    def __str__(self):
        # return f"{self.user_name}({self.full_name})"
        return f"{self.user.user_name}"


class ContactBook(models.Model):
    """ 10、*user_contact_book - 用户联系簿表 [1-N] """
    user = models.ForeignKey(BaseInfo, verbose_name='用户', related_name="user_set", db_constraint=False,
                             on_delete=models.DO_NOTHING, help_text='')
    # user_id = models.IntegerField(verbose_name='用户', help_text='')
    friend = models.ForeignKey(BaseInfo, verbose_name='朋友', related_name="friend_set", db_constraint=False,
                               on_delete=models.DO_NOTHING, help_text='待删')
    phone = models.JSONField(verbose_name='手机号', blank=True, null=True, help_text='')
    phones = models.JSONField(verbose_name='多个手机号', blank=True, null=True, help_text='')
    telephone = models.JSONField(verbose_name='电话号码', blank=True, null=True, help_text='')
    telephones = models.JSONField(verbose_name='多个电话号码', blank=True, null=True, help_text='')
    email = models.EmailField(verbose_name='邮箱', unique=True, blank=True, null=True, db_index=True, help_text='邮箱')
    qq = models.CharField(verbose_name='QQ', max_length=255, blank=True, null=True, help_text='')
    address = models.CharField(verbose_name='地址', max_length=255, blank=True, null=True, help_text='')
    more = models.JSONField(verbose_name='更多', blank=True, null=True, help_text='')
    remarks = models.CharField(verbose_name='标记', max_length=255, blank=True, null=True, help_text='')

    class Meta:
        db_table = prefix + 'user_contact_book'
        verbose_name_plural = "10. 用户 - 联系簿表"

    def __str__(self):
        # return f"{self.user_name}({self.full_name})"
        return f"{self.user_name}"


class UserSsoServe(models.Model):
    """ 11、User_Sso_Serve - 用户单点登录服务表 [NF1] """
    sso_code = models.CharField(verbose_name='单点登录代码', max_length=255, blank=True, null=True, help_text='')
    sso_name = models.CharField(verbose_name='单点登录名', max_length=255, blank=True, null=True, help_text='')
    sso_url = models.CharField(verbose_name='单点登录地址', max_length=255, blank=True, null=True, help_text='')
    sso_appid = models.CharField(verbose_name='AppID', max_length=255, blank=True, null=True, help_text='')
    sso_account = models.ForeignKey(BaseInfo, verbose_name='单点登录绑定账户', db_column='sso_account_id',
                                    db_constraint=False, on_delete=models.DO_NOTHING, help_text='')
    description = models.CharField(verbose_name='描述', max_length=255, blank=True, null=True, help_text='')

    class Meta:
        db_table = prefix + 'user_sso_serve'
        verbose_name_plural = "11. 用户 - 单点登录服务表"

    def __str__(self):
        # return f"{self.user_name}({self.full_name})"
        return f"{self.sso_code}"


class UserSsoToUser(models.Model):
    """ 12、User_Sso_To_User - 多对多单点登录记录表 [NF1] """
    sso_serve = models.ForeignKey(UserSsoServe, verbose_name='单点登录服务ID', db_constraint=False,
                                  on_delete=models.DO_NOTHING, help_text='')
    user = models.ForeignKey(BaseInfo, verbose_name='用户', db_constraint=False, on_delete=models.DO_NOTHING,
                             help_text='')
    sso_unicode = models.CharField(verbose_name='单点登录地址', max_length=255, blank=True, null=True, help_text='')
    sso_ticket = models.CharField(verbose_name='描述', max_length=255, blank=True, null=True, help_text='')
    union_code = models.CharField(verbose_name='微信唯一ID', max_length=255, blank=True, null=True, help_text='')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    is_delete = models.BooleanField(verbose_name='是否删除', default=False)

    class Meta:
        db_table = prefix + 'user_sso_to_user'
        verbose_name_plural = "12. 用户 - 多对多单点登录记录表"

    def __str__(self):
        return f"{self.sso_unicode}"


class UserRelateType(models.Model):
    """ 13、User_Relate_Type - 用户关系类型表 """
    id = models.AutoField(verbose_name='ID', primary_key=True)
    relate_key = models.CharField(verbose_name='关系搜索key', max_length=50, blank=True, null=True, default="",
                                  help_text='')
    relate_name = models.CharField(verbose_name='关系搜索名称', max_length=50, blank=True, null=True, default="",
                                   help_text='')
    is_multipeople = models.BooleanField(verbose_name="是否多人", default=0)
    description = models.CharField(verbose_name='关系描述', max_length=255, blank=True, null=True, default="",
                                   help_text='')

    class Meta:
        db_table = prefix + 'user_relate_type'
        verbose_name_plural = "13. 用户 - 关系类型表"

    def __str__(self):
        return f"{self.relate_key}"


class UserRelateToUser(models.Model):
    """ 14、User_Relate_To_User - 多对多关系类型表 """
    id = models.AutoField(verbose_name='ID', primary_key=True)
    user = models.ForeignKey(BaseInfo, verbose_name='关系人', blank=True, null=True, db_constraint=False, help_text='',
                             on_delete=models.DO_NOTHING)
    with_user = models.ForeignKey(BaseInfo, verbose_name='关联关系人', related_name="relate_with_user_id_alias",
                                  db_constraint=False, blank=True, null=True, help_text='', on_delete=models.DO_NOTHING)
    user_relate_type = models.ForeignKey(to=UserRelateType, verbose_name='关系类型ID', blank=True, null=True,
                                         db_constraint=False, on_delete=models.DO_NOTHING, help_text='', )
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, blank=True, null=True, )

    class Meta:
        db_table = prefix + 'user_relate_to_user'
        verbose_name_plural = "14. 用户 - 多对多关系类型表"

    def __str__(self):
        return f"{self.id}-{self.with_user_id}"


class UserBankCards(models.Model):
    id = models.AutoField(verbose_name='ID', primary_key=True)
    user = models.ForeignKey(to="BaseInfo", verbose_name='开户人', blank=True, null=True, help_text='',
                             db_constraint=False, on_delete=models.DO_NOTHING)
    bank_card_num = models.CharField(verbose_name='银行卡号', max_length=50, blank=True, null=True, help_text='', )
    open_account_bank = models.CharField(verbose_name='开户银行', max_length=50, blank=True, null=True, help_text='')
    opening_branch = models.CharField(verbose_name='开户支行', max_length=50, blank=True, null=True, help_text='')
    is_default = models.BooleanField(verbose_name='是否默认卡', blank=True, null=True, help_text='')
    ext = models.JSONField(verbose_name='扩展数据', blank=True, null=True, help_text='')
    sort = models.IntegerField(verbose_name='排序', blank=True, null=True, help_text='')
    remark = models.CharField(verbose_name='备注', max_length=500, blank=True, null=True, help_text='')

    class Meta:
        db_table = prefix + 'user_bank_cards'
        verbose_name_plural = "15. 用户 - 用户银行卡信息"

    def __str__(self):
        return f"{self.bank_card_num}"


class UserDevice(models.Model):
    class Meta:
        db_table = prefix + 'user_device'
        verbose_name_plural = "16. 用户 - 设备信息"

    id = models.AutoField(verbose_name='ID', primary_key=True)
    user = models.ForeignKey(to="BaseInfo", verbose_name='用户', blank=True, null=True, help_text='', db_constraint=False,
                             on_delete=models.DO_NOTHING)
    client_id = models.CharField(verbose_name='推送ID', max_length=50, blank=True, null=True, help_text='', )
    system = models.CharField(verbose_name='设备系统', max_length=20, blank=True, null=True, help_text='')
    ip = models.CharField(verbose_name='IP', max_length=255, blank=True, null=True, help_text='')
    device_model = models.CharField(verbose_name='设备型号', max_length=255, blank=True, null=True, help_text='')
    update_time = models.DateTimeField(verbose_name='更新时间', blank=True, null=True, help_text='')
    create_time = models.DateTimeField(verbose_name='创建时间', blank=True, null=True, help_text='')

    def __str__(self):
        return f"{self.user_id}"


class UserApplyType(models.Model):
    class Meta:
        db_table = prefix + 'user_apply_type'
        verbose_name_plural = "17. 用户 - 审批类型"

    id = models.AutoField(verbose_name='ID', primary_key=True)
    value = models.CharField(verbose_name='推送ID', max_length=50, blank=True, null=True, help_text='', )
    type_name = models.CharField(verbose_name='审批备注', max_length=500, blank=True, null=True, help_text='')
    description = models.CharField(verbose_name='拒绝理由', max_length=500, blank=True, null=True, help_text='')
    config = models.JSONField(verbose_name='快照', blank=True, null=True, help_text='')

    def __str__(self):
        return f"{self.id}"


class UserApplyRecord(models.Model):
    class Meta:
        db_table = prefix + 'user_apply_record'
        verbose_name_plural = "18. 用户 - 审批记录"

    id = models.AutoField(verbose_name='ID', primary_key=True)
    apply_type = models.ForeignKey(to="UserApplyType", verbose_name='审批类型', blank=True, null=True, help_text='',
                                   on_delete=models.DO_NOTHING)
    user = models.ForeignKey(BaseInfo, verbose_name='发起审批用户', blank=True, null=True, db_constraint=False,
                             on_delete=models.DO_NOTHING)
    verify_user = models.ForeignKey(BaseInfo, verbose_name='审批用户', on_delete=models.DO_NOTHING,
                                    related_name="verify_user_info", db_constraint=False, blank=True, null=True)
    result = models.CharField(verbose_name='审批结果', max_length=255, blank=True, null=True, help_text='')
    remark = models.CharField(verbose_name='审批备注', max_length=500, blank=True, null=True, help_text='')
    reject_reason = models.CharField(verbose_name='拒绝理由', max_length=500, blank=True, null=True, default="",
                                     help_text='')
    snapshot = models.JSONField(verbose_name='快照', blank=True, null=True, default={}, help_text='')
    verify_files = models.JSONField(verbose_name='审核文件集', blank=True, null=True, default={}, help_text='')
    verify_time = models.DateTimeField(verbose_name='审批时间', blank=True, null=True, help_text='')
    updated_time = models.DateTimeField(verbose_name='更新时间', auto_now=True, blank=True, null=True, help_text='')
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, blank=True, null=True, help_text='')

    def __str__(self):
        return f""


class UserSubCompany(models.Model):
    class Meta:
        db_table = prefix + 'user_subcompany'
        verbose_name_plural = "19. 用户 - 分子公司"

    id = models.AutoField(verbose_name='ID', primary_key=True)
    name = models.CharField(verbose_name='名称', max_length=100, blank=True, null=True, help_text='', )
    sort = models.IntegerField(verbose_name='排序', blank=True, null=True, help_text='')
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, blank=True, null=True, help_text='')
    updated_time = models.DateTimeField(verbose_name='更新时间', auto_now=True, blank=True, null=True, help_text='')

    def __str__(self):
        return f"{self.id}"
