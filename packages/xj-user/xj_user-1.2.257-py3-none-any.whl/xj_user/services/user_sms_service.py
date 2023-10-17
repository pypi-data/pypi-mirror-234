# encoding: utf-8
"""
@project: djangoModel->Auth
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 小程序SDK
@created_time: 2022/7/7 9:38
"""
import json
import sys
from logging import getLogger
from pathlib import Path

from django.forms import model_to_dict
import requests

from main.settings import BASE_DIR
if 'xj_role' in sys.modules:
    from xj_role.services.user_group_service import UserGroupService
from xj_user.services.login_service import LoginService
from xj_user.services.wechat_service import WechatService
from ..models import BaseInfo
from ..services.user_detail_info_service import DetailInfoService, write_to_log
from ..services.user_relate_service import UserRelateToUserService
from ..utils.custom_tool import get_short_id
from ..utils.j_config import JConfig
from ..utils.j_dict import JDict
from ..utils.nickname_generate import gen_one_word_digit

module_root = str(Path(__file__).resolve().parent)
# 配置之对象
main_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_user"))
module_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_user"))

payment_main_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_payment"))
payment_module_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_payment"))

sub_appid = payment_main_config_dict.wechat_merchant_app_id or payment_module_config_dict.wechat_merchant_app_id or ""

sub_app_secret = payment_main_config_dict.wechat_merchant_app_secret or payment_module_config_dict.wechat_merchant_app_secret or ""

app_id = main_config_dict.app_id or module_config_dict.app_id or ""
app_secret = main_config_dict.secret or module_config_dict.secret or ""
jwt_secret_key = main_config_dict.jwt_secret_key or module_config_dict.jwt_secret_key or ""
expire_day = main_config_dict.expire_day or module_config_dict.expire_day or ""
expire_second = main_config_dict.expire_second or module_config_dict.expire_second or ""

logger = getLogger('log')


class UserSmsService:

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
        user_info = requests.get(
            'https://api.weixin.qq.com/sns/jscode2session',
            params=req_params,
            timeout=3,
            verify=False
        )
        return user_info.json()

    def phone_login(self, phone, login_code, sso_serve_id=None, platform_id=None, other_params=None):
        if other_params is None:
            other_params = {}
        # 根据手机号获取用户
        current_user = BaseInfo.objects.filter(phone=phone).first()
        # print(">>>用户信息 current_user ", current_user)

        # 根据小程序code换取openid
        wechat_openid = self.get_openid(code=login_code)

        if wechat_openid.get("openid", None) is None:
            return None, "获取 openid 失败,请检查code是否过期"

        openid = wechat_openid.get("openid", "")
        unionid = wechat_openid.get("unionid", "")

        if not sso_serve_id:
            return None, "单点登录不能为空"

        if not platform_id:
            return None, "平台不能为空"

        # 如果用户未注册 用手机号进行注册
        if not current_user:
            base_info = {
                'user_name': get_short_id(8),
                'nickname': gen_one_word_digit(),
                'phone': phone,
                'email': '',
            }
            BaseInfo.objects.create(**base_info)

            # 注册完成后 重新获取用户信息
            user_info_set = BaseInfo.objects.filter(phone=phone).first()
            user_info = model_to_dict(user_info_set)

            # 用户第一次登录即注册，允许添加用户的详细信息
            try:
                other_params.setdefault("user_id", user_info.get('id', None))
                other_params.setdefault("score", "5")  # 用户评分初始化，镖行天下业务逻辑
                data, detail_err = DetailInfoService.create_or_update_detail(other_params)
                if detail_err:
                    raise Exception(detail_err)
            except Exception as e:
                write_to_log(prefix="用户手机号登录,绑定详细信息异常", err_obj=e)

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
            sso_set, sso_err = LoginService.sso_verify_2(sso_serve_id, user_info.get('id', None), sub_appid, openid,
                                                          unionid)
            if sso_err:
                return None, sso_err

            # 生成登录token
            token = LoginService.make_token(user_info.get('id', None), phone, platform_id)

            # 创建用户登录信息，绑定token
            auth_set, auth_err = LoginService.bind_token(user_info.get('id', None), token)
            if auth_err:
                return None, auth_err
            return {'token': "Bearer " + auth_set.token, 'user_info': user_info}, None
        # 如果用户已经存在
        else:
            # 存在当前用户，直接进行授权
            user_info = model_to_dict(current_user)
            # 检验单点登录信息
            sso_set, sso_err = LoginService.sso_verify_2(sso_serve_id, user_info.get('id', None), sub_appid, openid,
                                                          unionid)
            if sso_err:
                return None, sso_err

            # 创建用户登录信息，绑定token
            token = LoginService.make_token(user_info.get('id', None), user_info.get('phone', None), platform_id)
            # 修改用户登录信息，绑定token
            auth_set, auth_err = LoginService.bind_token(user_id=user_info.get('id', None), token=token,
                                                         is_create=False)
            if auth_err:
                return None, auth_err

            # 绑定用户关系 邀请关系和收益关系
        # data, relate_err = UserRelateToUserService.bind_bxtx_relate(params=other_params, user_info=user_info)
        # if relate_err:
        #     logger.error(
        #         '绑定用户关系异常：' + str(relate_err) +
        #         ' \n当前用户ID:' + str(user_info.get("id", "")) +
        #         '\n detail_params:' + json.dumps(other_params)
        #     )

        return {'token': "Bearer " + auth_set.token, 'user_info': user_info}, None
