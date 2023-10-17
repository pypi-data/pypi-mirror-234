# encoding: utf-8
"""
@project: djangoModel->Auth
@author: 孙楷炎,高栋天
@Email: sky4834@163.com
@synopsis: 小程序SDK
@created_time: 2022/7/7 9:38
"""
from datetime import datetime, timedelta
import json
from logging import getLogger
from pathlib import Path

from django.contrib.auth.hashers import make_password
from django.core.cache import cache
from django.forms import model_to_dict
import jwt
import redis
import requests

from main.settings import BASE_DIR
from xj_role.services.user_group_service import UserGroupService
from .user_detail_info_service import DetailInfoService, write_to_log
from ..models import BaseInfo, Auth, UserSsoToUser
from ..services.user_relate_service import UserRelateToUserService
from ..utils.custom_tool import get_short_id
from ..utils.j_config import JConfig
from ..utils.j_dict import JDict
from ..utils.model_handle import parse_model
from ..utils.nickname_generate import gen_one_word_digit

module_root = str(Path(__file__).resolve().parent)
# 配置之对象
main_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_user"))
module_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_user"))

payment_main_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_payment"))
payment_module_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_payment"))

sub_appid = payment_main_config_dict.wechat_merchant_app_id or payment_module_config_dict.wechat_merchant_app_id or ""
sub_app_secret = payment_main_config_dict.wechat_merchant_app_secret or payment_module_config_dict.wechat_merchant_app_secret or ""
wechat_merchant_name = payment_main_config_dict.wechat_merchant_name or payment_module_config_dict.wechat_merchant_name or ""

app_id = main_config_dict.app_id or module_config_dict.app_id or ""
app_secret = main_config_dict.secret or module_config_dict.secret or ""

app_app_id = payment_main_config_dict.wechat_app_app_id or payment_module_config_dict.wechat_app_app_id or ""

jwt_secret_key = main_config_dict.jwt_secret_key or module_config_dict.jwt_secret_key or ""
expire_day = main_config_dict.expire_day or module_config_dict.expire_day or ""
expire_second = main_config_dict.expire_second or module_config_dict.expire_second or ""

redis_main_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="main"))
redis_module_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="main"))

redis_host = redis_main_config_dict.redis_host or redis_module_config_dict.redis_host or ""
redis_port = redis_main_config_dict.redis_port or redis_module_config_dict.redis_port or ""
redis_password = redis_main_config_dict.redis_password or redis_module_config_dict.redis_password or ""

# print(">", sub_appid)
logger = getLogger('log')


class WechatService:
    wx_login_url = "https://api.weixin.qq.com/sns/jscode2session"
    wx_token_url = 'https://api.weixin.qq.com/cgi-bin/token'
    wx_get_phone_url = "https://api.weixin.qq.com/wxa/business/getuserphonenumber"

    def __init__(self):
        self.login_param = {'appid': app_id, 'secret': app_secret, 'grant_type': 'authorization_code'}
        self.redis = redis.Redis(
            host=redis_host,
            port=redis_port,
            password=redis_password
        )

    def get_openid(self, code):
        """
        :param code（openid登录的code）:
        :return:(err,data)
        """
        req_params = {
            'appid': sub_appid,
            'secret': sub_app_secret,
            'js_code': code,
            'grant_type': 'authorization_code',
        }
        user_info = requests.get('https://api.weixin.qq.com/sns/jscode2session', params=req_params, timeout=3,
                                 verify=False)
        return user_info.json()

    def wechat_login(self, phone_code, login_code, sso_serve_id=None, platform_id=None, other_params=None):
        """
        过期续约就是重新登录
        :param other_params:
        :param code: 换取手机号码的code
        :return:(err,data)
        """

        # code 换取手机号
        if other_params is None:
            other_params = {}
        url = self.wx_get_phone_url + "?access_token={}".format(self.get_access_token()['access_token'])
        header = {'content-type': 'application/json'}
        response = requests.post(url, json={'code': phone_code}, headers=header).json()
        if not response['errcode'] == 0:
            return response['errmsg'], ""
        phone = response['phone_info']['phoneNumber']

        if not login_code:
            return None, "微信登录 login_code 必传"
        wechat_openid = self.get_openid(code=login_code)
        if wechat_openid.get("openid", None) is None:
            return None, "获取 openid 失败,请检查code是否过期"
        if not sso_serve_id:
            return None, "平台不能为空"

        openid = wechat_openid.get("openid", "")
        unionid = wechat_openid.get("unionid", "")

        # 通过换取的手机号判断用户是否存在
        current_user = BaseInfo.objects.filter(phone=phone).first()

        # 登录即注册操作
        if not current_user:
            # 用户不存在的时候，进行注册用户
            base_info = {
                'user_name': get_short_id(8),  # 第一次注册的时候给一个唯一的字符串作登录账号
                'nickname': gen_one_word_digit(),
                'phone': phone,
                'email': ''
            }
            BaseInfo.objects.create(**base_info)

            # 注册完成后 重新获取用户信息
            user_info_set = BaseInfo.objects.filter(phone=phone).first()
            user_info = model_to_dict(user_info_set)

            # 生成登录token
            token = WechatService.set_token(user_info.get('id', None), phone, platform_id)
            # 用户第一次登录即注册，允许添加用户的详细信息
            try:
                other_params.setdefault("user_id", user_info.get('id', None))
                other_params.setdefault("score", "5")  # 用户评分初始化，镖行天下业务逻辑 TODO 后期业务抽离，路程控制
                data, detail_err = DetailInfoService.create_or_update_detail(other_params)
                if detail_err:
                    raise Exception(detail_err)
            except Exception as e:
                logger.error('---首次登录写入用户详细信息异常：' + str(e) + '---')

            # 用户第一次登录即注册，绑定用户的分组ID
            try:
                group_id = other_params.get("group_id")
                if group_id:
                    data, err = UserGroupService.user_bind_group(user_id=user_info.get('id', None), group_id=group_id)
                    write_to_log(
                        prefix="group_id:" + str(other_params.get("group_id", "")) + "用户手机号登录，绑定部门ID异常",
                        content=err
                    )
            except Exception as err:
                write_to_log(
                    prefix="用户手机号登录，绑定部门ID异常",
                    content="group_id:" + str(other_params.get("group_id", "")),
                    err_obj=err
                )

            # 检验单点登录信息
            sso_set, sso_err = WechatService.sso_verify(sso_serve_id, user_info.get('id', None), sub_appid, openid,
                                                        unionid)
            if sso_err:
                return None, sso_err

            # 创建用户登录信息，绑定token
            auth_set, auth_err = WechatService.get_token(user_info.get('id', None), token)
            if auth_err:
                return None, auth_err
        else:
            # 用户存在的时候
            user_info = model_to_dict(current_user)

            sso_set, sso_err = WechatService.sso_verify(sso_serve_id, user_info.get('id', None), sub_appid, openid,
                                                        unionid)
            if sso_err:
                return None, sso_err

            token = WechatService.set_token(user_info.get('id', None), phone, platform_id)
            # 修改用户登录信息，绑定token
            auth_set, auth_err = WechatService.get_token(user_id=user_info.get('id', None), token=token,
                                                         is_create=False)
            if auth_err:
                return None, auth_err

        # 绑定用户关系 邀请关系和收益关系
        data, relate_err = UserRelateToUserService.bind_bxtx_relate(params=other_params, user_info=user_info)
        if relate_err:
            logger.error(
                '绑定用户关系异常：' + str(relate_err) +
                ' \n当前用户ID:' + str(user_info.get("id", "")) +
                '\n other_params:' + json.dumps(other_params or {})
            )

        return {'token': auth_set.token, 'user_info': user_info}, None

    @staticmethod
    def wechat_app_login(params):
        unionid = params.get("unionid")
        openid = params.get("openid", None)
        sso_serve_id = params.get("sso_serve_id", 1)
        phone_code = params.get('phone_code', None)
        phone = params.get("phone", None)
        detail_params = params.get("detail_params", None)
        appid = app_app_id
        platform_id = params.get("platform_id", None)
        sso = UserSsoToUser.objects.filter(union_code=unionid, sso_serve_id=sso_serve_id).first()

        if not sso:
            if phone:
                if phone_code is None:
                    return None, "验证码不能为空"
                cache_code = cache.get(phone)
                if phone_code != cache_code:
                    return None, "验证码错误"
                current_user = BaseInfo.objects.filter(phone=phone).first()
                if current_user:
                    user = model_to_dict(current_user)
                    sso_set, sso_err = WechatService.sso_verify(sso_serve_id, user.get('id', None), sub_appid,
                                                                openid, unionid)
                    if sso_err:
                        return None, sso_err

                    token = WechatService.set_token(user.get('id', None), phone, platform_id)
                    auth_set, err = WechatService.get_token(user.get('id', None), token)
                    if err:
                        return None, err

                    return {'token': auth_set.token, 'user_info': user}, None
                else:
                    base_info = {
                        'user_name': get_short_id(8),  # 第一次注册的时候给一个唯一的字符串作登录账号
                        'nickname': gen_one_word_digit(),
                        'phone': phone,
                        'email': '',
                    }
                    base_info = BaseInfo.objects.create(**base_info)
                    if sso_serve_id:
                        sso_set, err = WechatService.sso_verify(sso_serve_id, base_info.id, appid, openid, unionid)
                        if err:
                            return None, err
                    token = WechatService.set_token(base_info.id, phone, platform_id)
                    auth_set, err = WechatService.get_token(current_user.get('id', None), token)
                    if err:
                        return None, err
                    return {'token': auth_set.token, 'user_info': current_user}, None
            else:
                return None, "PHONE_NOT_NULL"
        else:
            sso_dict = model_to_dict(sso)
            current_user = BaseInfo.objects.filter(id=sso_dict.get("user", 0)).first()
            current_user = model_to_dict(current_user)
            token = WechatService.set_token(current_user.get('id', None), current_user.get('phone', None), platform_id)
            # 修改用户登录信息，绑定token
            auth_set, err = WechatService.get_token(user_id=current_user.get('id', None), token=token,
                                                    is_create=False)
            if err:
                return None, err

            # 绑定用户关系 邀请关系和收益关系
            # data, relate_err = UserRelateToUserService.bind_bxtx_relate(params=detail_params, user_info=current_user)
            # if relate_err:
            #     logger.error(
            #         '绑定用户关系异常：' + str(relate_err) +
            #         ' \n当前用户ID:' + str(current_user.get("id", "")) +
            #         '\n detail_params:' + json.dumps(detail_params or {})
            #     )

            return {'token': auth_set.token, 'user_info': current_user}, None

    # 生成单点登录记录
    @staticmethod
    def sso_verify(sso_serve_id, user_id, appid, sso_unicode, union_code):
        """
        生成单点登录记录
        :param sso_serve_id: 单点登录服务ID
        :param user_id: 用户ID
        :param appid: appid
        :param sso_unicode: 单点登录唯一识别码(微信openid)
        :param union_code: union_id
        :return: param_dict
        """
        sso = UserSsoToUser.objects.filter(
            user_id=user_id,
            sso_serve__sso_appid=appid
        ).first()
        if not sso:
            sso_data = {
                "sso_serve_id": sso_serve_id,
                "user_id": user_id,
                "sso_unicode": sso_unicode,
                "union_code": union_code
            }
            sso_set = UserSsoToUser.objects.create(**sso_data)
            if not sso_set:
                return None, "单点登录写入失败"
        sso_set = UserSsoToUser.objects.filter(
            user_id=user_id,
            sso_serve__sso_appid=appid
        ).first()
        if not sso_set:
            return None, "平台用户信息不存在"
        sso_set = model_to_dict(sso_set)
        if not sso_set.get("union_code", None):
            UserSsoToUser.objects.filter(
                user_id=user_id,
                sso_serve__sso_appid=appid
            ).update(union_code=union_code)
        return sso_set, None

    @staticmethod
    def set_token(user_id, account, platform_id):
        # 生成过期时间
        expire_timestamp = datetime.utcnow() + timedelta(
            days=7,
            seconds=0
        )
        # 返回token
        return jwt.encode(
            payload={'user_id': user_id, 'account': account, 'platform_id': platform_id, "exp": expire_timestamp},
            key=jwt_secret_key
        )

    def get_access_token(self):
        param = {
            'appid': sub_appid,
            'secret': sub_app_secret,
            'grant_type': 'client_credential'
        }
        response = requests.get(self.wx_token_url, param).json()
        return response

    # 查询用户信息
    @staticmethod
    def get_user_info(user_id):
        current_user = BaseInfo.objects.filter(id=user_id).first()
        if not current_user:
            return None, "用户信息查询失败"
        current_user = model_to_dict(current_user)
        return current_user, None

    # 绑定token
    @staticmethod
    def get_token(user_id, token, is_create=True):
        current_user = BaseInfo.objects.filter(id=user_id).first()
        current_user = model_to_dict(current_user)
        if is_create:
            auth = {
                'user_id': current_user.get("id", ""),
                'password': make_password('123456', None, 'pbkdf2_sha1'),
                'plaintext': '123456',
                'token': token,
            }
            Auth.objects.update_or_create({'user_id': current_user.get("id", "")}, **auth)
            auth_set = Auth.objects.filter(user_id=current_user.get("id", ""),
                                           token__isnull=False).order_by(
                '-update_time').first()
        else:
            auth = {
                'token': token,
            }
            Auth.objects.update_or_create({'user_id': current_user.get("id", "")}, **auth)
            auth_set = Auth.objects.filter(
                user_id=current_user.get('id', None),
                token__isnull=False
            ).order_by('-update_time').first()

        if not auth_set:
            return None, "密钥生成失败"
        return auth_set, None

    def __del__(self):
        self.redis.close()
