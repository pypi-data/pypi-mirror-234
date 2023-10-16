# _*_coding:utf-8_*_

from datetime import datetime, timedelta
from pathlib import Path
import re

from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.db.models import Q, F
import jwt
from typing import Tuple, Dict, Any
from rest_framework import serializers

from config.config import JConfig as MainConfig
from main.settings import BASE_DIR
from ..models import Auth, Platform
from ..models import BaseInfo
from ..services.user_detail_info_service import DetailInfoService, get_short_id
from ..utils.custom_tool import filter_result_field, format_params_handle, format_list_handle
from ..utils.j_config import JConfig
from ..utils.j_dict import JDict

module_root = str(Path(__file__).resolve().parent)
# 配置之对象
main_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_user"))
module_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_user"))

app_id = main_config_dict.app_id or module_config_dict.app_id or ""
app_secret = main_config_dict.secret or module_config_dict.secret or ""
jwt_secret_key = main_config_dict.jwt_secret_key or module_config_dict.jwt_secret_key or ""
expire_day = main_config_dict.expire_day or module_config_dict.expire_day or ""
expire_second = main_config_dict.expire_second or module_config_dict.expire_second or ""

config = MainConfig()


class UserInfoSerializer(serializers.ModelSerializer):
    # 方法一：使用SerializerMethodField，并写出get_platform, 让其返回你要显示的对象就行了
    # p.s.SerializerMethodField在model字段显示中很有用。
    # platform = serializers.SerializerMethodField()

    # # 方法二：增加一个序列化的字段platform_name用来专门显示品牌的name。当前前端的表格columns里对应的’platform’列要改成’platform_name’
    user_id = serializers.ReadOnlyField(source='id')
    permission_value = serializers.SerializerMethodField()

    # platform_id = serializers.ReadOnlyField(source='platform.platform_id')
    # platform_name = serializers.ReadOnlyField(source='platform.platform_name')

    class Meta:
        model = BaseInfo
        fields = [
            'user_id',
            # 'platform',
            # 'platform_uid',
            # 'platform__platform_name',
            # 'platform_id',
            # 'platform_name',
            # 'get_group_desc',
            'user_name',
            'full_name',
            'phone',
            'email',
            'wechat_openid',
            'user_info',
            'user_group',
            'user_group_id',
            'permission',
            'permission_value'
        ]
        # exclude = ['platform_uid']

    def get_permission_value(self, instance):
        pass

    # # 这里是调用了platform这个字段拼成了get_platform
    # def get_platform(self, obj):
    #     return obj.platform.platform_name
    #     # return {
    #     #     'id': obj.platform.platform_id,
    #     #     'name': obj.platform.platform_name,
    #     # }


class UserService:
    def __init__(self):
        pass

    # 检测账户
    @staticmethod
    def check_account(account: str) -> Tuple[dict, str]:
        """
        :param {str} account: 用户账户，可以支持三种类型：手机、用户名、邮箱。自动判断
        :return: (user_info: {user_id, user_name, full_name, nickname, phone, email, wechat_openid, user_info}, error_text: str)
        :description 注意：用户名不推荐由纯数字构成，因为那样容易和11位手机号冲突
        """
        # 账号类型判断
        if re.match(r'(^1[356789]\d{9}$)|(^\+?[78]\d{10}$)', account):
            account_type = 'phone'
        elif re.match(r'^\w+[\w\.\-\_]*@\w+[\.\w]*\.\w{2,}$', account):
            account_type = 'email'
        elif re.match(r'^[A-z\u4E00-\u9FA5]+\w*$', account):
            account_type = 'username'
        else:
            return None, "账号必须是用户名、手机或者邮箱，用户名不能是数字开头"

        # 用户ID
        user_list = BaseInfo.objects.filter(Q(user_name=account) | Q(phone=account) | Q(email=account)) \
            .annotate(user_id=F("id")).values('user_id', 'user_name', 'full_name', 'nickname', 'phone', 'email', 'wechat_openid', 'user_info')
        if not user_list.count():
            return None, "账户不存在"
        if user_list.count() > 1:
            return None, "登录异常，请联系管理员，发现多账号冲突："
        user_set = user_list.first()
        return user_set, None

    # 验证密码
    @staticmethod
    def check_login(user_id, password, account, platform):
        """
        @param user_id 用户ID
        @param password 用户密码。
        @param account 登陆账号，必填，用于生成Token令牌。
        @description 注意：目前密码是明文传输，今后都要改成密文传输
        """
        # 检查平台是否存在
        platform_id = ""
        if platform:
            platform_set = Platform.objects.filter(platform_name__iexact=platform)
            if platform_set.count() is 0:
                return None, "platform不存在平台名称：" + platform
                # raise MyApiError("platform不存在平台名称："+platform, 2009)
            platform_id = platform_set.first().platform_id

        auth_set = Auth.objects.filter(user_id=user_id, password__isnull=False).order_by('-update_time').first()
        if not auth_set:
            return None, "账户尚未开通登录服务：" + account + "(" + str(user_id) + ")"

        # 判断密码不正确
        is_pass = check_password(password, auth_set.password)
        if not is_pass:
            return None, "密码错误"

        # print(int(Config.getIns().get('xj_user', 'DAY', 7)))
        # print(Config.getIns().get('xj_user', 'JWT_SECRET_KEY', ""))

        # 过期时间
        # int(Config.getIns().get('xj_user', 'DAY', 7))
        # int(Config.getIns().get('xj_user', 'SECOND', 0))
        expire_timestamp = datetime.utcnow() + timedelta(days=7, seconds=0)
        # 为本次登录生成Token并记录
        # todo 漏洞，当用户修改用户名时，并可能导致account失效，是否存用户ID更好
        token = jwt.encode(
            payload={'account': account, 'user_id': user_id, 'platform_id': platform_id, 'exp': expire_timestamp},
            key=jwt_secret_key)
        # payload = jwt.decode(token, key=Config.getIns().get('xj_user', 'JWT_SECRET_KEY', ""), verify=True, algorithms=["RS256", "HS256"])
        # print("> payload:", payload)
        auth_set.token = token
        auth_set.save()

        return {'token': token}, None

    # 微信登录
    '''
    @staticmethod
    def check_login_wechat(user_id, phone):
        """
        @param user_id 用户ID
        @param phone 登陆账号，必填，用于生成Token令牌。
        @description 注意：目前密码是明文传输，今后都要改成密文传输
        """
        auth_set = Auth.objects.filter(user_id=user_id, password__isnull=False).order_by('-update_time').first()
        if not auth_set:
            return None, "账户尚未开通登录服务：" + phone + "(" + str(user_id) + ")"

        # 过期时间
        expire_timestamp = datetime.utcnow() + timedelta(days=7, seconds=0)
        # 为本次登录生成Token并记录
        # todo 漏洞，当用户修改用户名时，并可能导致account失效，是否存用户ID更好
        token = jwt.encode(payload={'account': phone, 'user_id': user_id, "exp": expire_timestamp}, key=jwt_secret_key)
        # payload = jwt.decode(token, key=Config.getIns().get('xj_user', 'JWT_SECRET_KEY'), verify=True, algorithms=["RS256", "HS256"])
        # print("> payload:", payload)
        auth_set.token = token
        auth_set.save()

        return {'token': token}, None
    '''

    # 验证密码
    '''
    @staticmethod
    def check_login_short(user_id, phone):
        """
        @param user_id 用户ID
        @param phone 登陆账号，必填，用于生成Token令牌。
        @description 注意：目前密码是明文传输，今后都要改成密文传输
        """
        auth_set = Auth.objects.filter(user_id=user_id, password__isnull=False).order_by('-update_time').first()
        if not auth_set:
            return None, "账户尚未开通登录服务：" + phone + "(" + str(user_id) + ")"

        # 过期时间
        expire_timestamp = datetime.utcnow() + timedelta(days=int(expire_day),
                                                         seconds=int(expire_second))
        # 为本次登录生成Token并记录
        # todo 漏洞，当用户修改用户名时，并可能导致account失效，是否存用户ID更好
        token = jwt.encode(payload={'account': phone, 'user_id': user_id, "exp": expire_timestamp}, key=jwt_secret_key)
        # payload = jwt.decode(token, key=Config.getIns().get('xj_user', 'JWT_SECRET_KEY'), verify=True, algorithms=["RS256", "HS256"])
        # print("> payload:", payload)
        auth_set.token = token
        auth_set.save()

        return {'token': token}, None
    '''

    # 检测令牌
    @staticmethod
    def check_token(token):
        """
        @param token 用户令牌。
        @description 注意：用户令牌的载荷体payload中必须包含两个参数：account账号、exp过期时间，其中账号可以是手机、用户名、邮箱三种。
        @description BEARER类型的token是在RFC6750中定义的一种token类型，OAuth2.0协议RFC6749对其也有所提及，算是对RFC6749的一个补充。BEARER类型token是建立在HTTP/1.1版本之上的token类型，需要TLS（Transport Layer Security）提供安全支持，该协议主要规定了BEARER类型token的客户端请求和服务端验证的具体细节。
        @description 理论上，每次请求令牌后就更新一次令牌，以监测用户长期访问时，不至于到时间后掉线反复登陆。
        """
        # 检查是否有Bearer前辍，如有则截取
        # print("> token 1:", token)
        if not token:
            return None, "请登录"  # 缺少Token

        if re.match(r'Bearer(.*)$', token, re.IGNORECASE):
            token = re.match(r'Bearer(.*)$', token, re.IGNORECASE).group(1).strip()
        # print("> token 2:", token)

        if not token:
            return None, "您尚未登录"

        # # 验证token。另一种方式，从数据库核对Token，通过对比服务端的Token，以确定是否为服务器发送的。今后启用该功能。
        # auth_set = Auth.objects.filter(Q(token=token)).order_by('-update_time')
        # # print("> auth:", auth_set)
        # if not auth_set.count():
        #     raise MyApiError('token验证失败', 6002)
        # auth = auth_set.first()

        try:
            # jwt.decode会自动检查exp参数，如果超时则抛出jwt.ExpiredSignatureError超时
            # jwt_payload = jwt.decode(token, key=Config.getIns().get('xj_user', 'JWT_SECRET_KEY'), verify=True, algorithms=["RS256", "HS256"])
            jwt_payload = jwt.decode(token, key=config.get('xj_user', 'JWT_SECRET_KEY', '@zxmxy2021!'),
                                     verify=True, algorithms=["RS256", "HS256"])
            # print("> jwt_payload:", jwt_payload)

        except jwt.ExpiredSignatureError:
            return None, "登录已过期，请重新登录"

        except jwt.InvalidTokenError:
            return None, "用户令牌无效，请重新登录"

        account = jwt_payload.get('account', None)
        user_id = jwt_payload.get('user_id', None)
        platform_id = jwt_payload.get('platform_id', None)
        if not account:
            return {'payload': jwt_payload}, "错误：令牌载荷中未提供用户账户Account"

        # 检测用户令牌时不应该调用用户信息，这会导致任何接口都会查询用户表，时间会增加
        # user_info = UserService.check_account(account=account)

        return {'account': account, 'user_id': user_id, 'platform_id': platform_id}, None

    # 用户信息列表
    @staticmethod
    def user_list(params=None, allow_user_list=None, ban_user_list=None, need_Pagination=True):
        """
        用户基础信息列表服务
        :param params: 搜索字典参数 dict
        :param allow_user_list: 允许用户ID列表 list
        :param ban_user_list: 不允许用户ID列表 list
        :param need_Pagination: 是否需要分页 bool
        :return: {size: int, page: int, count: int, list:list<dict>}, err: str
        """
        if params is None:
            params = {}
        user_base_set = BaseInfo.objects
        # 需要分页的时候
        page = params.get("page", 1)
        size = params.get("size", 20)

        # 允许筛选的字段
        user_name = params.get("user_name", None)
        email = params.get("email", None)
        phone = params.get("phone", None)
        full_name = params.get("full_name", None)
        nickname = params.get("nickname", None)

        # 用户信息排序
        sort = params.get("sort", "-id")
        sort = sort if sort in ["id", "-id", "register_time", "-register_time"] else "-id"
        user_base_set = user_base_set.order_by(sort)

        # 开始按过滤条件
        try:
            user_base_set = user_base_set.annotate(user_id=F("id"))
            if allow_user_list:  # 筛选可以访问的列表
                user_base_set = user_base_set.filter(user_id__in=allow_user_list)
            if ban_user_list:  # 排除可以访问的列表
                user_base_set = user_base_set.filter(~Q(user_id__in=ban_user_list))
            if user_name:
                user_base_set = user_base_set.filter(user_name=user_name)
            if email:
                user_base_set = user_base_set.filter(email=email)
            if phone:
                user_base_set = user_base_set.filter(phone=phone)
            if full_name:
                user_base_set = user_base_set.filter(full_name__icontains=full_name)
            if nickname:
                user_base_set = user_base_set.filter(user_name__icontains=nickname)

            user_base_set = user_base_set.values(
                "user_id", "email", "full_name", "user_name", "nickname", "phone", "register_time", "wechat_openid",
            )
            count = user_base_set.count()
            # 查询保护，当超过100条的时候则需要分页查询
            if not need_Pagination and count <= 100:
                return list(user_base_set), None
        except Exception as e:
            return None, "err:" + e.__str__()
        page_set = Paginator(user_base_set, size).page(page)
        return {'size': int(size), 'page': int(page), 'count': count, 'list': list(page_set.object_list)}, None

    @staticmethod
    def user_add(params):
        """
        用户添加服务
        :param params: 添加参数
        :return: data,err
        """
        try:
            account = str(params.get('account', ''))
            password = str(params.get('password', ''))
            full_name = str(params.get('full_name', ''))
            nickname = str(params.get('nickname', ''))
            # 边界检查
            if not account:
                return None, "account必填"
            # 账号类型判断
            if re.match(r'(^1[356789]\d{9}$)|(^\+?[78]\d{10}$)', account):
                account_type = 'phone'
            elif re.match(r'^\w+[\w\.\-\_]*@\w+[\.\w]*\.\w{2,}$', account):
                account_type = 'email'
            elif re.match(r'^[A-z\u4E00-\u9FA5]+\w*$', account):
                account_type = 'username'
            else:
                return None, "账号必须是手机、邮箱格式或者为纯英文且不含特殊字符12位字符"
            # 检查账号是否存在
            user_list = None
            if account_type == 'phone':
                user_list = BaseInfo.objects.filter(Q(phone=account))
            elif account_type == 'email':
                user_list = BaseInfo.objects.filter(Q(email=account))
            elif account_type == 'username':
                user_list = BaseInfo.objects.filter(Q(user_name=account))

            if user_list.count() and account_type == 'phone':
                return None, "手机已被注册: " + account
            elif user_list.count() and account_type == 'email':
                return None, "邮箱已被注册: " + account
            elif user_list.count() and account_type == 'username':
                return None, "用户名已被注册: " + account

            # 创建基础信息
            base_info = {
                'user_name': account if account_type == 'username' else get_short_id(),
                'phone': account if account_type == 'phone' else "",
                'email': account if account_type == 'email' else '',
                'full_name': full_name,
                "nickname": nickname,
            }
            current_user = BaseInfo.objects.create(**base_info)
            # 创建登录信息
            token = jwt.encode({'account': account}, jwt_secret_key)
            auth = {
                'user_id': current_user.id,
                'password': make_password(password, None, 'pbkdf2_sha1'),
                'plaintext': password,
                'token': token,
            }
            Auth.objects.create(**auth)
            return {"user_id": current_user.id}, None
        except SyntaxError:
            return None, "语法错误"
        except LookupError:
            return None, "无效数据查询"
        except Exception as valueError:
            return None, valueError.msg if hasattr(valueError, 'msg') else valueError.args
        except:
            return None, "未知错误"

    @staticmethod
    def user_edit(params: dict = None, user_id: [int, str] = None):
        """
        用户基础信息修改服务。
        PS:不允许修改用户的用户名，用户名负责登录作用
        :param params: 修改参数集合
        :param user_id: 用户ID
        :return: None,err_msg
        """
        if params is None:
            params = {}
        if not user_id:
            return None, "用户ID不存在"

        # 绑定信息验重
        email_other_user = BaseInfo.objects.exclude(id=user_id).filter(email=params.get("email", None)).first()
        if params.get("email") and email_other_user:
            return None, "当前邮箱被绑定"
        phone_other_user = BaseInfo.objects.exclude(id=user_id).filter(phone=params.get("phone", None)).first()
        if params.get("phone") and phone_other_user:
            return None, "当前手机号被绑定"

        # 用户基础信息中仅仅可以修改一下参数
        # PS:邮箱和手机号不能为空，所以需要user_name不可修改，而且最初登录使用user_name。然后可以绑定
        base_info_params = format_params_handle(
            param_dict=params.copy(),
            filter_filed_list=["full_name", "nickname", "user_info", "email", "phone"],
            is_remove_null=True
        )
        # 更新基础信息
        base_query_set = BaseInfo.objects.filter(id=user_id)
        if not base_query_set.first():
            return None, "用户不存在"
        try:
            base_query_set.update(**base_info_params)
        except Exception as e:
            return None, "修改异常：" + str(e)

        # 详细信息
        detail_info_params = format_params_handle(
            param_dict=params.copy(),
            remove_filed_list=["full_name", "nickname", "user_info"]
        )
        detail_info_params.setdefault("user_id", user_id)
        data, err = DetailInfoService.create_or_update_detail(detail_info_params)
        if err:
            return None, "详情修改异常：" + err
        return None, None

    @staticmethod
    def user_delete(id):
        if not id:
            return None, "ID 不能为空"
        try:
            BaseInfo.objects.filter(id=id).delete()
        except Exception as e:
            return None, e
        return None, None

    @staticmethod
    def user_search(user_id_list: list = None, search_params: dict = None, need_map: bool = False, filter_fields: list = None):
        """
        搜索用户，返回用户基础信息列表，没有分页限制。服务调用不做接口
        :param user_id_list: 用户id列表
        :param search_params: 搜素条件
        :param need_map: 是否需要映射
        :param filter_fields: 在返回数据中筛选字段列表
        :return: data, err
        """
        if not user_id_list:
            return [], "缺少用户id列表"  # 参数错误,无法筛选数据

        if not search_params:
            return [], "缺少用户的搜索条件"  # 参数错误,无法筛选数据

        # 列表的查询参数处理
        if filter_fields is None:
            filter_fields = ["id", "user_name", "full_name", "nickname", "phone", "email", "register_time"]
        else:
            filter_fields = format_list_handle(
                param_list=filter_fields,
                filter_filed_list=["id", "user_name", "full_name", "nickname", "phone", "email", "register_time"]
            )
            filter_fields = ["id", "user_name", "full_name", "nickname", "phone", "email", "register_time"] if not filter_fields else filter_fields

        # 字段查询参数处理
        if search_params:
            search_params = format_params_handle(
                param_dict=search_params,
                filter_filed_list=["id", "user_id", "user_name", "full_name", "nickname", "phone", "email", "register_time", "register_time_start", "register_time_end"],
                alias_dict={"user_id": "id", "register_time_start": "register_time__gte", "register_time_end": "register_time_lte"}
            )

            search_params = make_queries_condition(
                param_dict=search_params,
                filter_filed_list=["id", "user_id", "user_name", "full_name", "nickname", "phone", "email",
                                   "register_time", "register_time_start", "register_time_end"],
                alias_dict={"user_id": "id", "register_time_start": "register_time__gte",
                            "register_time_end": "register_time_lte"}
            )

        # 查询管理
        try:
            # orm 查询
            if user_id_list:
                user_base_set = BaseInfo.objects.filter(id__in=user_id_list)
            else:
                user_base_set = BaseInfo.objects.filter(**search_params)
            user_base_set = user_base_set.values(*filter_fields)
            # 获取列表并字段转换，id ==>> user_id
            user_base_list = filter_result_field(
                result_list=list(user_base_set),
                alias_dict={"id": "user_id"}
            )
            # 如果需要转换，则进行映射
            if need_map:
                user_base_list = {i['user_id']: i for i in user_base_list}
            return user_base_list, None
        except Exception as e:
            return [], "err:" + str(e)
