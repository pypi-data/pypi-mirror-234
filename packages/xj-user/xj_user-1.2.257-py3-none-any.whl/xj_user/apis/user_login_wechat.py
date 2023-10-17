# encoding: utf-8
"""
@project: djangoModel->wechet_login
@author: 孙楷炎
@created_time: 2022/7/14 10:55
"""

# 微信登录方法
from logging import getLogger

from rest_framework.views import APIView

from ..services.wechat_service import WechatService
from ..utils.custom_response import util_response
from ..utils.custom_tool import request_params_wrapper, flow_service_wrapper

logger = getLogger('log')


class WechetLogin(APIView):
    # 微信手机号码登录
    @request_params_wrapper
    @flow_service_wrapper
    def post(self, *args, request_params, **kwargs):
        phone_code = request_params.get('phone_code', None)
        login_code = request_params.get('login_code', None)
        sso_serve_id = request_params.get('sso_serve_id', None)
        platform_id = request_params.get('platform_id', None)
        if not phone_code:
            return util_response(err=6558, msg='参数错误')
        app = WechatService()
        data, err = app.wechat_login(phone_code=phone_code, login_code=login_code, sso_serve_id=sso_serve_id,
                                     platform_id=platform_id,
                                     other_params=request_params)
        if data:
            return util_response(data=data)
        else:
            logger.error('---登录错误：' + str(err) + '---')
            return util_response(msg=err, err=6004)
