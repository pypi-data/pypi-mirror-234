# encoding: utf-8
"""
@project: djangoModel->wechet_login
@author:
@created_time: 2022/7/14 10:55
"""
# 微信登录方法
from logging import getLogger

from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from ..services.login_service import LoginService
from ..services.user_main_service import UserMainService
from ..utils.custom_response import util_response
from ..utils.custom_tool import request_params_wrapper, flow_service_wrapper, write_to_log
from ..utils.user_wrapper import user_authentication_wrapper

logger = getLogger('log')


class UserLoginMain(APIView):

    @api_view(['POST'])
    @request_params_wrapper
    @flow_service_wrapper
    def login_main(self, *args, request_params=None, **kwargs):
        response = HttpResponse()
        response.status_code = 200
        if request_params is None:
            request_params = {}
        logger.info('---用户登录参数打印：' + str(request_params) + '---')

        data, err = UserMainService.login_integration_interface(request_params)
        if err:
            if isinstance(err, dict) and err.get("error"):
                content = util_response(data=err['wechat_data'], msg=err['msg'], err=int(err['error']))
            else:
                content = util_response(err=4002, msg=err)
        else:
            # 判斷賬號
            if data["user_info"]["is_using"] != 1:
                response.content = util_response(err=4002, msg="该账号禁止登录")
                return response
            content = util_response(data=data)
            response['Authorization'] = data.get("token", "")
        response.content = content
        return response

    @api_view(['POST'])
    @user_authentication_wrapper
    @request_params_wrapper
    def bind_phone(self, *args, user_info, request_params, **kwargs, ):
        params = request_params
        user_id = user_info.get("user_id")
        bind_phone, err = LoginService.bind_phone(user_id, params.get("phone", ""))
        if err is None:
            return util_response(data=bind_phone)
        return util_response(err=47767, msg=err)

    @api_view(['POST'])
    @user_authentication_wrapper
    @request_params_wrapper
    def wechat_unbinding(self, *args, user_info, request_params, **kwargs, ):
        params = request_params
        user_id = user_info.get("user_id")
        wechat_unbinding, err = LoginService.wechat_unbinding(params)
        if err is None:
            return util_response(data=wechat_unbinding)
        return util_response(err=47767, msg=err)

    @api_view(['POST'])
    @user_authentication_wrapper
    @request_params_wrapper
    def secondary_authorization(self, *args, user_info, request_params, **kwargs, ):
        params = request_params
        user_id = user_info.get("user_id")
        params.setdefault("user_id", user_id)  # 用户ID
        empower, err = LoginService.secondary_authorization(params)
        if err is None:
            return util_response(data=empower)
        return util_response(err=47767, msg=err)

    # @api_view(['POST'])
    # @request_params_wrapper
    # def send(self, *args, request_params=None, **kwargs):
    #     params = request_params
    #     parameter = "{'account':%s,'pwd':%s}" % (123, 456)
    #     bind_phone, err = LoginService.template_send("applet", "register", )
    #     if err is None:
    #         return util_response(data=bind_phone)
    #     return util_response(err=47767, msg=err)

    @api_view(['POST'])
    @request_params_wrapper
    @flow_service_wrapper
    def register(self, *args, request_params=None, **kwargs):
        response = HttpResponse()
        response.status_code = 200
        if request_params is None:
            request_params = {}
        data, err = UserMainService.register(request_params)
        if err is None:
            return util_response(data=data)
        return util_response(err=47767, msg=err)
