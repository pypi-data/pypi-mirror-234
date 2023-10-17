import re
import sys
import uuid
from datetime import datetime, timedelta
import json
from logging import getLogger
from pathlib import Path
import string
import random
import jwt
from django.core.cache import cache
from django.db.models import Q, F
from django.forms import model_to_dict
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.sessions.models import Session

from main.settings import BASE_DIR
from xj_captcha.services.sms_service import SmsService
if 'xj_role' in sys.modules:
    from xj_role.services.user_group_service import UserGroupService
# from xj_user.apis.user_platform import UserPlatform
from xj_user.services.user_detail_info_service import DetailInfoService
from xj_user.services.user_relate_service import UserRelateToUserService
# from xj_user.services.user_service import UserService
# from xj_user.utils.wechat_sign import applet_subscribe_message, subscribe_message
from xj_user.utils.custom_tool import get_short_id, write_to_log
from xj_user.utils.nickname_generate import gen_one_word_digit
from xj_user.utils.wechat import get_openid
from ..models import BaseInfo, Auth, UserSsoToUser, Platform, PlatformsToUsers, UserSsoServe
from ..utils.j_config import JConfig
from ..utils.j_dict import JDict
from ..utils.utility_method import generate_password, replace_placeholders

module_root = str(Path(__file__).resolve().parent)
# 配置之对象
main_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_user"))
module_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_user"))

payment_main_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_payment"))
payment_module_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_payment"))

sub_appid = payment_main_config_dict.wechat_merchant_app_id or payment_module_config_dict.wechat_merchant_app_id or ""
sub_app_secret = payment_main_config_dict.wechat_merchant_app_secret or payment_module_config_dict.wechat_merchant_app_secret or ""
wechat_merchant_name = payment_main_config_dict.wechat_merchant_name or payment_module_config_dict.wechat_merchant_name or ""

app_id = payment_main_config_dict.app_id or payment_module_config_dict.app_id or ""
app_secret = payment_main_config_dict.secret or payment_module_config_dict.secret or ""

subscription_app_id = payment_main_config_dict.wechat_subscription_app_id or payment_module_config_dict.wechat_subscription_app_id or ""
subscription_app_secret = payment_main_config_dict.wechat_subscription_app_secret or payment_module_config_dict.wechat_subscription_app_secret or ""

app_app_id = payment_main_config_dict.wechat_app_app_id or payment_module_config_dict.wechat_app_app_id or ""
app_app_secret = payment_main_config_dict.wechat_app_app_secret or payment_module_config_dict.wechat_app_app_secret or ""

apple_app_id = payment_main_config_dict.apple_app_id or payment_module_config_dict.apple_app_id or ""

jwt_secret_key = main_config_dict.jwt_secret_key or module_config_dict.jwt_secret_key or ""
expire_day = main_config_dict.expire_day or module_config_dict.expire_day or ""
expire_second = main_config_dict.expire_second or module_config_dict.expire_second or ""
template = main_config_dict.template or module_config_dict.template or ""

redis_main_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="main"))
redis_module_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="main"))

redis_host = redis_main_config_dict.redis_host or redis_module_config_dict.redis_host or ""
redis_port = redis_main_config_dict.redis_port or redis_module_config_dict.redis_port or ""
redis_password = redis_main_config_dict.redis_password or redis_module_config_dict.redis_password or ""


class LoginService:
    @staticmethod
    def sso_record(user_id, appid):
        sso_set = UserSsoToUser.objects.filter(
            user_id=user_id,
            sso_serve__sso_appid=appid
        ).first()
        if not sso_set:
            return None, "查询用户信息失败"
        return model_to_dict(sso_set), None

    # 生成单点登录记录
    @staticmethod
    def sso_verify(sso_serve_id, user_id, appid, is_exist=True, sso_unicode=None, union_code=None):
        """
        生成单点登录记录
        :param sso_serve_id: 单点登录服务ID
        :param user_id: 用户ID
        :param appid: appid
        :param sso_unicode: 单点登录唯一识别码(微信openid)
        :param union_code: union_id
        :return: param_dict
        """
        sso_initialize = UserSsoToUser.objects

        query_dict = {}
        where_dict = {}
        query_dict['is_delete'] = 0
        query_dict['sso_serve_id'] = sso_serve_id

        where_dict['is_delete'] = 0

        if user_id:
            query_dict['user_id'] = user_id
            sso_initialize = sso_initialize.filter(~Q(user_id=user_id))

        # 短信验证码登录和正常登录方式是不会存在openid、appid、union_code
        if sso_unicode:
            query_dict['sso_serve__sso_appid'] = appid
            query_dict['sso_unicode'] = sso_unicode
            where_dict['sso_unicode'] = sso_unicode
            where_dict['sso_serve__sso_appid'] = appid

        if union_code:
            where_dict['union_code'] = union_code
            where_dict.pop("sso_unicode", 100)
            where_dict.pop("sso_serve__sso_appid", 100)

        sso = UserSsoToUser.objects.filter(**query_dict).order_by(
            '-id').first()
        # 创建并查询
        if is_exist:
            # 如果检查不到登录信息则创建
            if not sso:
                sso_data = {
                    "sso_serve_id": sso_serve_id,
                    "user_id": user_id,
                    "sso_unicode": sso_unicode,
                    "union_code": union_code
                }
                create_sso = UserSsoToUser.objects.create(**sso_data)
                if not create_sso:
                    return None, "单点登录写入失败"
            # 创建成功后进行查询 再一次确认创建成功
            sso_set = UserSsoToUser.objects.filter(**query_dict).order_by(
                '-id').first()
            if not sso_set:
                return None, "单点登录用户信息不存在"
            sso_set = model_to_dict(sso_set)
            # 重置老单点登录信息
            # UserSsoToUser.objects.filter(**query_dict).filter(~Q(id=sso_set.get("id", ""))).update(
            #     is_delete=1)
            # 如果没查询到微信unionid 并且传入了如果没查询到微信unionid 则更新
            if not sso_set.get("union_code", "") and union_code:
                UserSsoToUser.objects.filter(
                    is_delete=0,
                    user_id=user_id,
                    sso_serve__sso_appid=appid
                ).update(union_code=union_code)
        else:
            sso_set = sso_initialize.filter(**where_dict).order_by(
                '-id').first()

            if not sso_set:
                return {"user": 0}, "单点记录不存在（微信）"
            sso_set = model_to_dict(sso_set)

        return sso_set, None

    # 生成token
    @staticmethod
    def make_token(user_id, account, platform_id, platform_code=None):
        # 生成过期时间
        expire_timestamp = datetime.utcnow() + timedelta(
            days=7,
            seconds=0
        )
        # 返回token
        return jwt.encode(
            payload={'user_id': user_id, 'account': account, 'platform_id': platform_id, "platform_code": platform_code,
                     "exp": expire_timestamp},
            key=jwt_secret_key
        )

    # 绑定token
    @staticmethod
    def bind_token(user_id, token, is_create=True, password=None):
        if is_create:
            auth = {
                'user_id': user_id,
                'password': make_password(password, None, 'pbkdf2_sha1'),
                'plaintext': password,
                'token': token,
            }
        else:
            auth = {
                'token': token,
            }
        Auth.objects.update_or_create({'user_id': user_id}, **auth)
        auth_set = Auth.objects.filter(
            user_id=user_id,
            token__isnull=False
        ).order_by('-update_time').first()

        if not auth_set:
            return None, "密钥生成失败"
        return auth_set, None

    # ------------------------登录类型判断----------------------------------------------
    @staticmethod
    def type_judgment(login_type, account, phone, password, platform_code, sms_code, user_id, code, phone_code,
                      sso_serve_id, bind_data={}, apple_logo=None):
        """
         登录类型判断
         :param login_type: 登录类型
         :param account: 账户
         :param phone: 手机号
         :param password: 密码
         :param platform_code: 平台码
         :param sms_code: 手机验证码
         :param user_id: 用户ID
         :param code: 微信code
         :param phone_code: 微信手机code
         :param sso_serve_id: 单点登录id
         :param sso_serve_code: 平台码
         :param bind_data: 绑定数据
         :return: param_dict
        """
        # 初始化
        user_info_set = BaseInfo.objects
        user_info_set = user_info_set.extra(
            select={'register_time': 'DATE_FORMAT(register_time, "%%Y-%%m-%%d %%H:%%i:%%s")'})

        sso_app_id = ""
        openid = ""
        unionid = ""
        wechat = {}
        wx_login_type = ""  # 登录类型

        if login_type == "PASSWORD":  # 账号登录
            wx_login_type = "pwd"
            account = str(account)
            if re.match(r'(^1[356789]\d{9}$)|(^\+?[78]\d{10}$)', account):
                current_user_count = user_info_set.filter(**{"phone": account, "is_delete": 0}).count()
                if current_user_count > 1:
                    return None, {"error": "0", "msg": "您输入的用户存在多账号信息，请通过验证码登录",
                                  "wechat_data": {"error": "6666"}}
            account_serv, error_text = LoginService.check_account(account, platform_code)
            if error_text:
                return None, error_text
            user_id = account_serv['id']

            auth_serv, auth_error = LoginService.check_login(user_id=user_id, password=password, )

            if auth_error:
                return None, auth_error

            current_user = user_info_set.filter(**{"id": auth_serv['user_id'], "is_delete": 0}).first()

        elif login_type == "SMS":  # 短信验证码登录 (比较特殊 支持多用户)
            wx_login_type = "sms"
            sms, sms_err = SmsService.check_sms({"phone": phone, "sms_code": sms_code})
            if sms_err and not user_id:
                return None, sms_err
            current_user_count = user_info_set.filter(**{"phone": phone, "is_delete": 0}).count()
            if current_user_count > 1 and not user_id:
                current_user = user_info_set.extra(select={
                    'avatar': 'SELECT avatar FROM user_detail_info WHERE user_base_info.id = user_detail_info.user_id'})
                current_user = current_user.filter(**{"phone": phone, "is_delete": 0}).values("id", "user_name",
                                                                                              "avatar")
                return {'token': "", 'user_info': list(current_user)}, None
            elif user_id:
                current_user = user_info_set.filter(**{"id": user_id, "is_delete": 0}).first()
            else:
                current_user = user_info_set.filter(**{"phone": phone, "is_delete": 0}).first()

        elif login_type == "WECHAT_APPLET":  # 小程序登录
            wx_login_type = "applet"
            wechat['appid'] = sub_appid
            wechat['secret'] = sub_app_secret
            wechat['code'] = code
            wechat['phone_code'] = phone_code
            sso_app_id = wechat['appid']
            wechat_user_info, err = get_openid(login_type, wechat)
            if err:
                return None, err
            openid = wechat_user_info.get("openid", "")
            unionid = wechat_user_info.get("unionid", "")
            phone = wechat_user_info.get("phone", "")
            sso_set, sso_err = LoginService.sso_verify(sso_serve_id=sso_serve_id, user_id=None, appid=sso_app_id,
                                                       is_exist=False,
                                                       sso_unicode=openid,
                                                       union_code=unionid)

            if sso_set and not (user_info_set.filter(**{"id": sso_set['user'], "is_delete": 0}).first()):
                current_user = user_info_set.filter(**{"phone": phone, "is_delete": 0}).first()
            elif sso_set:
                current_user = user_info_set.filter(**{"id": sso_set['user'], "is_delete": 0}).first()
            else:
                current_user = user_info_set.filter(**{"phone": phone, "is_delete": 0}).first()

        elif login_type == "WECHAT_WEB":  # 公众号
            wx_login_type = "subscribe"
            wechat['appid'] = subscription_app_id
            wechat['secret'] = subscription_app_secret
            wechat['code'] = code
            sso_app_id = wechat['appid']
            wechat_user_info, err = get_openid(login_type, wechat)
            if err:
                return None, err
            openid = wechat_user_info.get("openid", "")
            unionid = wechat_user_info.get("unionid", "")
            sso_set, sso_err = LoginService.sso_verify(sso_serve_id=sso_serve_id, user_id=None, appid=sso_app_id,
                                                       is_exist=False,
                                                       sso_unicode=openid,
                                                       union_code=unionid)
            current_user = user_info_set.filter(**{"id": sso_set['user'], "is_delete": 0}).first()

        elif login_type == "WECHAT_APP":  # APP
            wx_login_type = "app"
            wechat['appid'] = app_app_id
            wechat['secret'] = app_app_secret
            wechat['code'] = code
            sso_app_id = wechat['appid']
            wechat_user_info, err = get_openid(login_type, wechat)
            if err:
                return None, err
            openid = wechat_user_info.get("openid", "")
            unionid = wechat_user_info.get("unionid", "")
            sso_set, sso_err = LoginService.sso_verify(sso_serve_id=sso_serve_id, user_id=None, appid=sso_app_id,
                                                       is_exist=False,
                                                       sso_unicode=openid,
                                                       union_code=unionid)
            current_user = user_info_set.filter(**{"id": sso_set['user'], "is_delete": 0}).first()
        elif login_type == "APPLE":  # 苹果APP
            wx_login_type = "apple"
            sso_app_id = apple_app_id
            openid = apple_logo
            sso_set, sso_err = LoginService.sso_verify(sso_serve_id=sso_serve_id, user_id=None, appid=sso_app_id,
                                                       is_exist=False,
                                                       sso_unicode=openid,
                                                       union_code=None)
            current_user = user_info_set.filter(**{"id": sso_set['user'], "is_delete": 0}).first()
        else:
            return None, "未支持登录方式"
        return {'user_info': current_user, 'phone': phone, 'appid': sso_app_id, 'openid': openid,
                'unionid': unionid, "wx_login_type": wx_login_type}, None

    # -----------------------登录逻辑处理-----------------------------------------------
    @staticmethod
    def logical_processing(current_user, phone, sso_serve_id, sso_app_id, openid, unionid, platform_id, platform_code,
                           other_params, wx_login_type):
        """
          登录逻辑处理
          :param current_user: 用户数据
          :param phone: 手机号
          :param sso_serve_id: 单点登录id
          :param sso_app_id: 单点登录app_id
          :param openid: openid
          :param unionid: unionid
          :param platform_id: 平台id
          :param platform_code: 平台code
          :return: param_dict
        """
        suuid = uuid.uuid1()
        is_create = True
        if not current_user:  # 如果不存在则为注册
            base_info = {
                'user_name': get_short_id(8),
                'nickname': gen_one_word_digit(),
                'phone': phone,
                'email': '',
                "uuid": str(suuid).replace("-", ""),
                "user_type": "PERSON",
                "is_delete": 0
            }
            create_user = BaseInfo.objects.create(**base_info)
            if not create_user:
                return None, "用户注册失败"
            # 注册完成后 重新获取用户信息
            user_info_set = BaseInfo.objects.filter(id=create_user.id).first()
            user_info = model_to_dict(user_info_set)
            if platform_id:
                platforms_users = PlatformsToUsers.objects.create(**{
                    "platform_id": platform_id,
                    "user_id": user_info.get('id', "")
                })
                if not platforms_users:
                    return None, "平台写入失败"
        else:
            is_create = False
            # 用户存在的时候
            user_info = model_to_dict(current_user)
        # ----------------------------------------------------------------------
        # 多对多模型没法转换成字典 直接在此处踢出
        user_info.pop("platforms_to_users")

        # 检查单点登录信息（查询并创建）针对小程序、公众号、APP，同一微信平台绑定过的绑定
        if sso_serve_id:
            sso_set, sso_err = LoginService.sso_verify(sso_serve_id=sso_serve_id, user_id=user_info.get('id', ""),
                                                       appid=sso_app_id,
                                                       is_exist=True,
                                                       sso_unicode=openid,
                                                       union_code=unionid)
            if sso_err:
                return None, sso_err

        # TODO token可以考虑让各个子服务独立获取token，而不是公共生成Token，当然，这样设计好不好有待商考 20230507 by Sieyoo
        token = LoginService.make_token(user_info.get('id', ""), user_info.get("user_name", ""), platform_id,
                                        platform_code)
        password = generate_password(12)
        # 修改用户登录信息，绑定token
        auth_set, auth_err = LoginService.bind_token(user_id=user_info.get('id', ""), token=token,
                                                     is_create=is_create, password=password)
        if auth_err:
            return None, auth_err

        if is_create:
            # 注册成功后发送短信通知
            sms_data = {
                "phone": phone,
                "platform": 'ALi',
                "account": user_info.get("user_name", ""),
                "pwd": password,
                "type": "PWD"
            }

            if wx_login_type == "applet" or wx_login_type == "sms":
                sms_set, sms_err = SmsService.bid_send_sms(sms_data)
                if sms_err:
                    write_to_log(
                        prefix="首次登录写入用户详细信息异常",
                        content='---首次登录写入用户详细信息异常：' + str(sms_err) + '---',
                        err_obj=sms_err
                    )

            try:
                other_params.setdefault("user_id", user_info.get('id', ""))
                other_params.setdefault("score", "5")  # 用户评分初始化，镖行天下业务逻辑 TODO 后期业务抽离，路程控制
                data, detail_err = DetailInfoService.create_or_update_detail(other_params)
                if detail_err:
                    raise Exception(detail_err)
            except Exception as e:
                write_to_log(
                    prefix="首次登录写入用户详细信息异常",
                    content='---首次登录写入用户详细信息异常：' + str(e) + '---',
                    err_obj=e
                )
            # 用户第一次登录即注册，绑定用户的分组ID
            try:
                group_id = other_params.get("group_id")
                if group_id:
                    data, err = UserGroupService.user_bind_group(user_id=user_info.get('id', ""), group_id=group_id)
                    write_to_log(
                        prefix="group_id:" + str(other_params.get("group_id", "")) + "绑定部门ID异常",
                        content=err
                    )
            except Exception as err:
                write_to_log(
                    prefix="绑定部门ID异常",
                    content="group_id:" + str(other_params.get("group_id", "")),
                    err_obj=err
                )
        else:
            # 绑定用户关系 邀请关系和收益关系
            data, relate_err = UserRelateToUserService.bind_bxtx_relate(params=other_params, user_info=user_info)
            if relate_err:
                write_to_log(
                    prefix='绑定用户关系异常：' + str(relate_err),
                    content='当前用户ID:' + str(user_info.get("id", "")) + '\n detail_params:' + json.dumps(
                        other_params),
                    err_obj=relate_err
                )

        return {'token': "Bearer " + auth_set.token, 'user_info': user_info}, None

    # 验证账户
    @staticmethod
    def check_account(account, platform_code, type=None):
        """
        @param account 用户账户，可以支持三种类型：手机、用户名、邮箱。自动判断
        @description 注意：用户名不推荐由纯数字构成，因为那样容易和11位手机号冲突
        """
        # 账号类型判断
        if re.match(r'(^1[356789]\d{9}$)|(^\+?[78]\d{10}$)', account):
            account_type = 'phone'
        elif re.match(r'^\w+[\w\.\-\_]*@\w+[\.\w]*\.\w{2,}$', account):
            account_type = 'email'
        elif re.match(r'^[A-Za-z\u4E00-\u9FA5_0-9]\w*$', account):
            account_type = 'username'
        else:
            return None, "账号必须是手机、邮箱格式或者为纯英文且不含特殊字符12位字符"
        user_list = BaseInfo.objects.filter(Q(user_name=account) | Q(phone=account) | Q(email=account)).annotate(
            user_id=F("id"))
        if platform_code:
            user_list = user_list.filter(Q(platforms_to_users__platform_code=platform_code), Q(is_delete=0))
        else:
            user_list = user_list.exclude(Q(platforms_to_users__user_id__isnull=False), Q(is_delete=0))
        if type:
            if user_list.count():
                return None, "用户名已被注册"
            else:
                return None, None
        if not user_list.count():
            return None, "账户不存在"
        user_set = user_list.first()
        user = model_to_dict(user_set)
        return user, None

    # 检查密码
    @staticmethod
    def check_login(user_id, password):
        """
        @param user_id 用户ID
        @param password 用户密码。
        @param account 登陆账号，必填，用于生成Token令牌。
        @description 注意：目前密码是明文传输，今后都要改成密文传输
        """

        # 检查平台是否存在
        where = {
            "user_id": user_id,
            "password__isnull": False
        }

        auth_set = Auth.objects.filter(**where).order_by('-update_time').first()
        if not auth_set:
            return None, "账户尚未开通登录服务：" + user_id + "(" + str(user_id) + ")"

        # 判断密码不正确
        is_pass = check_password(password, auth_set.password)
        if not is_pass:
            return None, "密码错误"

        return {"user_id": user_id}, None

    # 绑定手机号
    @staticmethod
    def bind_phone(user_id, phone):
        """
        @param user_id 用户ID
        @param phone 手机号
        """
        if not phone:
            return None, "手机号不能为空1"
        mate = re.match(r'(^1[356789]\d{9}$)|(^\+?[78]\d{10}$)', phone)
        if not mate:
            return None, "手机号格式不正确"

        binding_verification, err = LoginService.phone_binding_verification(phone)
        if err:
            return None, err
        bind_user = BaseInfo.objects.filter(id=user_id).update(**{
            "phone": phone
        })
        if not bind_user:
            return None, "用户绑定手机号失败，请联系管理员处理"
        return {"user_id": user_id, "phone": phone}, None

    # 手机绑定验证 一个手机号最多绑定5个账户
    @staticmethod
    def phone_binding_verification(phone):
        """
        @param phone 手机号
        """
        if not phone:
            return None, "手机号不能为空2"
        mate = re.match(r'(^1[356789]\d{9}$)|(^\+?[78]\d{10}$)', phone)
        if not mate:
            return None, "手机号格式不正确"
        bind_user = BaseInfo.objects.filter(**{"phone": phone, "is_delete": 0}).count()
        if bind_user >= 1:
            # return None, "同一手机号最多绑定5个账户,已绑定" + str(bind_user) + "个"
            return None, "该手机号已被其他账号绑定"
        return {"phone": phone, "bind_num": bind_user}, None

    # 二次授权
    @staticmethod
    def secondary_authorization(params):
        """
        @param user_id 用户ID
        @param code 微信code
        """
        user_id = params.get("user_id", "")
        sso_serve_id = params.get("sso_serve_id", "")
        login_type = params.get("login_type", "")
        code = params.get("code", "")
        sso_code = params.get("sso_code", "")
        if not sso_serve_id and sso_code:
            sso_serve = UserSsoServe.objects.filter(sso_code=sso_code).first()
            sso_serve_id = sso_serve.id
        wechat = {}

        if login_type == "WECHAT_APPLET":  # 小程序
            wechat['appid'] = sub_appid
            wechat['secret'] = sub_app_secret
            wechat['code'] = code
            sso_app_id = wechat['appid']
            wechat_user_info, err = get_openid(login_type, wechat)
            if err:
                return None, err
            openid = wechat_user_info.get("openid", "")
            unionid = wechat_user_info.get("unionid", "")

        elif login_type == "WECHAT_WEB":  # 公众号
            wechat['appid'] = subscription_app_id
            wechat['secret'] = subscription_app_secret
            wechat['code'] = code
            sso_app_id = wechat['appid']
            wechat_user_info, err = get_openid(login_type, wechat)
            if err:
                return None, err
            openid = wechat_user_info.get("openid", "")
            unionid = wechat_user_info.get("unionid", "")

        elif login_type == "WECHAT_APP":  # APP
            wechat['appid'] = app_app_id
            wechat['secret'] = app_app_secret
            wechat['code'] = code
            sso_app_id = wechat['appid']
            wechat_user_info, err = get_openid(login_type, wechat)
            if err:
                return None, err
            openid = wechat_user_info.get("openid", "")
            unionid = wechat_user_info.get("unionid", "")

        sso_exist, sso_exist_err = LoginService.sso_verify(sso_serve_id=sso_serve_id, user_id=user_id,
                                                           appid=sso_app_id,
                                                           is_exist=False,
                                                           sso_unicode=openid,
                                                           union_code=None)

        if sso_exist_err:
            sso_set, sso_err = LoginService.sso_verify(sso_serve_id=sso_serve_id, user_id=user_id, appid=sso_app_id,
                                                       is_exist=True,
                                                       sso_unicode=openid,
                                                       union_code=unionid)
        else:
            return None, "微信已被绑定"

        if sso_err:
            return None, "绑定失败"
        return sso_set, None

    @staticmethod
    def wechat_unbinding(params):
        user_id = params.get("user_id", "")
        login_type = params.get("login_type", "")
        if login_type == "WECHAT_APPLET":  # 小程序
            UserSsoToUser.objects.filter(
                is_delete=0,
                user_id=user_id,
                sso_serve__sso_appid=sub_appid
            ).update(is_delete=1)
        elif login_type == "WECHAT_WEB":  # 公众号
            UserSsoToUser.objects.filter(
                is_delete=0,
                user_id=user_id,
                sso_serve__sso_appid=subscription_app_id
            ).update(is_delete=1)
        elif login_type == "WECHAT_APP":  # APP
            UserSsoToUser.objects.filter(
                is_delete=0,
                user_id=user_id,
                sso_serve__sso_appid=app_app_id
            ).update(is_delete=1)

        return None, None

    # 注册信息写入
    @staticmethod
    def register_write(account, nickname, phone, platform_id, platform_code, password):
        base_info = {
            'user_name': account,
            'nickname': nickname if nickname else gen_one_word_digit(),
            'phone': phone,
            "uuid": uuid.uuid1(),
            "user_type": "PERSON"
        }
        create_user = BaseInfo.objects.create(**base_info)
        if not create_user:
            return None, "用户注册失败"
        # 注册完成后 重新获取用户信息
        user_info_set = BaseInfo.objects.filter(id=create_user.id).first()
        user_info = model_to_dict(user_info_set)

        if platform_id:
            platforms_users = PlatformsToUsers.objects.create(**{
                "platform_id": platform_id,
                "user_id": user_info.get('id', "")
            })
            if not platforms_users:
                return None, "平台写入失败"
        token = LoginService.make_token(user_info.get('id', ""), user_info.get("user_name", ""),
                                        platform_id,
                                        platform_code)
        # 修改用户登录信息，绑定token
        auth_set, auth_err = LoginService.bind_token(user_id=user_info.get('id', ""), token=token,
                                                     is_create=True, password=password)
        if auth_err:
            return None, auth_err
        other_params = {}
        try:
            other_params.setdefault("user_id", user_info.get('id', ""))
            other_params.setdefault("score", "5")  # 用户评分初始化，镖行天下业务逻辑 TODO 后期业务抽离，路程控制
            data, detail_err = DetailInfoService.create_or_update_detail(other_params)
            if detail_err:
                raise Exception(detail_err)
        except Exception as e:
            write_to_log(
                prefix="首次登录写入用户详细信息异常",
                content='---首次登录写入用户详细信息异常：' + str(e) + '---',
                err_obj=e
            )
        return {'token': "Bearer " + auth_set.token, 'user_info': user_info}, None
