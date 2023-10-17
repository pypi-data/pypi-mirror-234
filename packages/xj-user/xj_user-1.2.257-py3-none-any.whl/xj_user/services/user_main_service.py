from django.forms import model_to_dict

from xj_user.utils.custom_tool import write_to_log
from ..models import Platform, UserSsoServe
from ..services.login_service import LoginService


class UserMainService:

    @staticmethod
    def register(params):
        platform_id = params.get("platform_id", None)  # 平台。不应该支持ID传入，无法数据移植。20230507 by Sieyoo
        platform_code = params.get("platform_code", None)
        account = params.get('account', '')
        nickname = params.get('nickname', '')
        phone = params.get('phone', '')
        password = str(params.get('password', ''))

        if platform_code:
            platform_set = Platform.objects.filter(platform_code=platform_code).first()
            if not platform_set:
                return None, "platform不存在平台名称：" + platform_code
            platform_id = model_to_dict(platform_set)['platform_id']

        if platform_id:
            platform_set = Platform.objects.filter(platform_id=platform_id).first()
            if not platform_set:
                return None, "所属平台不存在"
            platform_code = model_to_dict(platform_set)['platform_code']

        account_serv, error_text = LoginService.check_account(account, platform_code, "REGISTER")
        if error_text:
            return None, error_text

        register_serv, register_error = LoginService.register_write(account, nickname, phone, platform_id,
                                                                    platform_code, password)
        if register_error:
            return None, register_error

        return register_serv, None

    """
     登录整合接口，支持以下几种登录方式：
          1、PASSWORD 账户密码登录
          2、SMS 短信验证码登录 （支持多账号登录*）
          3、WECHAT_APPLET 微信小程序授权登录
          4、WECHAT_WEB 微信公众号授权登录
          5、WECHAT_APP 微信APP授权登录

    """

    @staticmethod
    def login_integration_interface(params):
        data = {}
        # ----------------------------获取信息----------------------------------------
        # TODO platform_id字段 即将弃用，改为platform_code 20230507 by Sieyoo
        platform_id = params.get("platform_id", None)  # 平台。不应该支持ID传入，无法数据移植。20230507 by Sieyoo
        platform_code = params.get("platform_code", None)
        user_id = params.get("user_id", None)  # 用户id
        login_type = params.get("login_type", None)  # 支持的登录方式
        code = params.get("code", None)  # 微信登录code
        phone_code = params.get("phone_code", None)  # 微信手机号code
        sms_code = params.get("sms_code", None)  # 短信验证码
        sso_serve_id = params.get("sso_serve_id", 1)  # 单点登录用户平台
        sso_serve_code = params.get("sso_serve_code", None)  # 单点登录用户平台
        phone = params.get("phone", None)  # 手机号
        other_params = params.get("other_params", None)
        account = params.get("account", None)  # 账户
        password = params.get("password", None)  # 密码
        bind_data = params.get("bind_data", None)  # 绑定的数据
        apple_logo = params.get("apple_logo", None)  # 苹果
        # ------------------------边界检查----------------------------------------------
        if not login_type:
            return None, "登录方式不能为空"
        if platform_code:
            platform_set = Platform.objects.filter(platform_code=platform_code).first()
            if not platform_set:
                return None, "platform不存在平台名称：" + platform_code
            platform_id = model_to_dict(platform_set)['platform_id']

        if platform_id:
            platform_set = Platform.objects.filter(platform_id=platform_id).first()
            if not platform_set:
                return None, "所属平台不存在"
            platform_code = model_to_dict(platform_set)['platform_code']

        if sso_serve_id:
            sso_server_set = UserSsoServe.objects.filter(id=sso_serve_id).first()
            if not sso_server_set:
                return None, "单点登录平台不存在：" + sso_serve_id
            sso_serve_id = model_to_dict(sso_server_set)['id']

        if sso_serve_code:
            sso_server_set = UserSsoServe.objects.filter(sso_code=sso_serve_code).first()
            if not sso_server_set:
                return None, "单点登录平台不存在：" + sso_serve_code
            sso_serve_id = model_to_dict(sso_server_set)['id']
        # ------------------------登录类型判断----------------------------------------------

        if other_params is None:
            other_params = {}
        try:
            current_user, user_err = LoginService.type_judgment(login_type, account, phone, password, platform_code,
                                                                sms_code, user_id, code, phone_code,
                                                                sso_serve_id, bind_data,apple_logo)
            if user_err:
                return None, user_err
            if isinstance(current_user.get("user_info", None), list):
                return current_user, None
            else:
                # print(">>>>>", current_user)
                data, err = LoginService.logical_processing(current_user.get("user_info", None),
                                                            current_user.get("phone", None), sso_serve_id,
                                                            current_user.get("appid", None),
                                                            current_user.get("openid", None),
                                                            current_user.get("unionid", None),
                                                            platform_id,
                                                            platform_code, other_params,
                                                            current_user.get("wx_login_type", None))
                if err:
                    return None, err
        except Exception as e:
            write_to_log(
                prefix="登录异常",
                content='---用户登录异常：' + str(e) + '---',
                err_obj=e
            )

        return data, None
