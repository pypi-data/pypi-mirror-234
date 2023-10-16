# encoding: utf-8
"""
@project: djangoModel->wechet_login
@author:
@created_time: 2022/7/14 10:55
"""

# 微信登录方法
from logging import getLogger

from rest_framework.views import APIView

from ..services.wechat_service import WechatService
from ..utils.custom_response import util_response
from ..utils.custom_tool import parse_data

logger = getLogger('log')


class WechetAppLogin(APIView):
    # 微信App登录
    def post(self, request):
        params = parse_data(request)
        app = WechatService()
        data, err = app.wechat_app_login(params=params)
        if data:
            return util_response(data=data)
        else:
            logger.error('---登录错误：' + err + '---')
            return util_response(msg=err, err=6004)
