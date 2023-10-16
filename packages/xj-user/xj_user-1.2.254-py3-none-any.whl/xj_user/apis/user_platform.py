# _*_coding:utf-8_*_

import logging

from rest_framework import generics
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ..models import Platform
from ..services.user_platform_service import UserPlatformService
from ..utils.custom_response import util_response
# from apps.finance.models import *
from ..utils.custom_tool import request_params_wrapper
from ..utils.user_wrapper import user_authentication_force_wrapper

logger = logging.getLogger(__name__)


class UserPlatformSerializer(serializers.ModelSerializer):
    value = serializers.ReadOnlyField(source='platform_name')
    platform = serializers.ReadOnlyField(source='platform_name')

    class Meta:
        model = Platform
        fields = [
            # 'platform_id',
            # 'platform_name',
            'value',
            'platform',
        ]


# 获取平台列表
# class UserPlatform(generics.UpdateAPIView):  # 或继承(APIView)
class UserPlatform(generics.UpdateAPIView):  # 或继承(APIView)
    """ REST framework的APIView实现获取card列表 """
    # authentication_classes = (TokenAuthentication,)  # token认证
    # permission_classes = (IsAuthenticated,)   # IsAuthenticated 仅通过认证的用户
    permission_classes = (AllowAny,)  # 允许所有用户 (IsAuthenticated,IsStaffOrBureau)
    serializer_class = UserPlatformSerializer
    params = None

    def get(self, request, *args, **kwargs):
        self.params = request.query_params  # 返回QueryDict类型

        platforms = Platform.objects.all()
        serializer = UserPlatformSerializer(platforms, many=True)
        return Response({
            'err': 0,
            'msg': 'OK',
            'data': serializer.data,
        })

    @request_params_wrapper
    def put(self, *args, request_params=None, **kwargs):
        if request_params is None:
            request_params = {}
        data, err = UserPlatformService.edit(params=request_params)
        if err:
            return util_response(err=1001, msg=err)
        return util_response(data=data)

    @request_params_wrapper
    def post(self, *args, request_params=None, **kwargs):
        if request_params is None:
            request_params = {}

        data, err = UserPlatformService.add(params=request_params)
        if err:
            return util_response(err=1001, msg=err)
        return util_response(data=data)

    @request_params_wrapper
    def delete(self, *args, request_params=None, **kwargs):
        if request_params is None:
            request_params = {}

        data, err = UserPlatformService.delete(params=request_params)
        if err:
            return util_response(err=1001, msg=err)
        return util_response()

    @api_view(["GET", "POST"])
    @request_params_wrapper
    def list(self, *args, request_params=None, **kwargs):
        if request_params is None:
            request_params = {}
        try:
            need_pagination = int(request_params.pop("need_pagination", 1))
        except ValueError:
            need_pagination = 1

        data, err = UserPlatformService.list(params=request_params, need_pagination=need_pagination)
        if err:
            return util_response(err=1001, msg=err)
        return util_response(data=data)

    @api_view(["GET", "POST"])
    @request_params_wrapper
    @user_authentication_force_wrapper
    def get_user_platform(self, *args, request_params=None, user_info=None, **kwargs):
        if user_info is None:
            user_info = {}
        if request_params is None:
            request_params = {}
        user_id = request_params.get("user_id", None) or user_info.get("user_id", None)
        data, err = UserPlatformService.get_platform_info_by_user_id(user_id=user_id)
        if err:
            return util_response(err=1001, msg=err)
        return util_response(data=data)
