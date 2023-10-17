from logging import getLogger

from django.core.cache import cache
from rest_framework import response
from rest_framework.views import APIView

from xj_captcha.services.sms_service import SmsService
from ..services.user_sms_service import UserSmsService
from ..utils.custom_response import util_response
from ..utils.custom_tool import request_params_wrapper, flow_service_wrapper

logger = getLogger('log')


class ShortMessageLogin(APIView):

    # 短信验证码校验
    @request_params_wrapper
    @flow_service_wrapper
    def sms_login(self, *args, request_params, **kwargs):
        # 1. 电话和手动输入的验证码
        # params = parse_data(self)
        phone = request_params.get('phone')
        code = request_params.get('code')
        login_code = request_params.get('login_code', None)
        sso_serve_id = request_params.get('sso_serve_id', None)
        platform_id = request_params.get('platform_id', None)
        if code is None:
            return util_response(err=4002, msg="验证码不能为空")
        # cache_code = cache.get(phone)
        sms, sms_err = SmsService.check_sms({"phone": phone, "sms_code": code})
        if sms_err:
            return None, sms_err
        # if code == cache_code:
        app = UserSmsService()
        data, err = app.phone_login(
            phone=phone,
            login_code=login_code,
            sso_serve_id=sso_serve_id,
            platform_id=platform_id,
            other_params=request_params,
        )
        if err:
            logger.error('---短信登录错误：' + err + '---')
            return util_response(msg=err, err=6004)

        return util_response(data=data)
        # else:
        #     return util_response(err=4002, msg="验证码错误")

    # 短信验证码校验
    def post(self, request):
        # 1. 电话和手动输入的验证码
        phone = request.POST.get('phone')
        code = request.POST.get('code')
        login_code = request.data.get('login_code', None)
        sso_serve_id = request.data.get('sso_serve_id', None)
        if code is None:
            res = {
                'err': 4002,
                'msg': '验证码不能为空',
            }
            return response.Response(data=res, status=None, template_name=None)
        cache_code = cache.get(phone)
        if code == cache_code:
            # if code == cache_code:
            app = UserSmsService()
            err, data = app.phone_login(phone=phone, login_code=login_code, sso_serve_id=sso_serve_id)
            if err == 0:
                return util_response(data=data)
            else:
                return util_response(msg=err, err=6004)
        else:
            res = {
                'err': 4002,
                'msg': '验证码错误0',
            }
            return response.Response(data=res, status=None, template_name=None)


class MyApiError(Exception):
    def __init__(self, message, err_code=4010):
        self.msg = message
        self.err = err_code

    def __str__(self):
        # repr()将对象转化为供解释器读取的形式。可省略
        return repr(self.msg)
