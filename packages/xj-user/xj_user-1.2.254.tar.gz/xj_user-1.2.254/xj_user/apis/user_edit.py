# _*_coding:utf-8_*_

import logging
from pathlib import Path

from rest_framework import generics
from rest_framework import serializers
from rest_framework.permissions import AllowAny

from main.settings import BASE_DIR
from ..models import *
from ..services.user_detail_info_service import request_params_wrapper, flow_service_wrapper
from ..services.user_service import UserService
from ..utils.custom_response import util_response
from ..utils.custom_tool import dynamic_load_class
from ..utils.j_config import JConfig
from ..utils.j_dict import JDict
from ..utils.user_wrapper import user_authentication_force_wrapper

module_root = str(Path(__file__).resolve().parent)
# 配置之对象
main_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_user"))
module_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_user"))

jwt_secret_key = main_config_dict.jwt_secret_key or module_config_dict.jwt_secret_key or ""

logger = logging.getLogger(__name__)


class UserInfoSerializer(serializers.ModelSerializer):
    # 方法一：使用SerializerMethodField，并写出get_platform, 让其返回你要显示的对象就行了
    # p.s.SerializerMethodField在model字段显示中很有用。
    # platform = serializers.SerializerMethodField()

    # # 方法二：增加一个序列化的字段platform_name用来专门显示品牌的name。当前前端的表格columns里对应的’platform’列要改成’platform_name’
    user_id = serializers.ReadOnlyField(source='id')

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
            'user_name',
            'full_name',
            'phone',
            'email',
            'wechat_openid',
            'user_info',
        ]
        # exclude = ['platform_uid']

    # 这里是调用了platform这个字段拼成了get_platform
    def get_platform(self, obj):
        return obj.platform.platform_name
        # return {
        #     'id': obj.platform.platform_id,
        #     'name': obj.platform.platform_name,
        # }


# 获取用户信息
class UserEdit(generics.UpdateAPIView):  # 或继承(APIView)
    permission_classes = (AllowAny,)  # 允许所有用户 (IsAuthenticated,IsStaffOrBureau)
    serializer_class = UserInfoSerializer
    params = None

    @user_authentication_force_wrapper
    @request_params_wrapper
    @flow_service_wrapper
    def user_edit(self, *args, user_info=None, request_params=None, **kwargs):
        if request_params is None:
            request_params = {}
        if user_info is None:
            user_info = {}

        user_id = request_params.pop("user_id", None) or user_info.get("user_id")  # 没有传则修改当前的用户的信息
        data, err = UserService.user_edit(params=request_params.copy(), user_id=user_id)

        # ------------------------ section 角色修改联动 start --------------------------------
        try:
            # 编辑角色服务
            RoleService, err = dynamic_load_class(
                import_path="xj_role.services.role_service",
                class_name="RoleService"
            )
            if not err and request_params.get("user_role_list"):
                data, err = RoleService.bind_user_roles(
                    user_id=request_params.get("user_id"),
                    role_list=request_params.get("user_role_list"),
                )

            # # 编辑部门服务
            UserGroupService, err = dynamic_load_class(
                import_path="xj_role.services.user_group_service",
                class_name="UserGroupService"
            )
            if not err and request_params.get("user_group_list"):
                data, err = UserGroupService.user_bind_groups(
                    user_id=request_params.get("user_id"),
                    group_list=request_params.get("user_group_list"),
                )
        except Exception as e:
            pass
        # ------------------------ section 角色修改联动 end   --------------------------------

        if err:
            return util_response(err=1000, msg=err)
        return util_response()

    @user_authentication_force_wrapper
    @request_params_wrapper
    def bind_identity(self, *args, user_info=None, request_params=None, **kwargs):
        if request_params is None:
            request_params = {}
        if user_info is None:
            user_info = {}

        user_id = request_params.pop("user_id", None) or user_info.get("user_id")  # 没有传则修改当前的用户的信息
        data, err = UserService.bind_user_identity(user_id=user_id, user_identity=request_params.get("user_identity"))
        if err:
            return util_response(err=1000, msg=err)
        data, err = UserService.user_edit(params=request_params.copy(), user_id=user_id)
        if err:
            return util_response(err=1000, msg=err)
        return util_response()

    # def delete(self, request, *args, **kwargs):
    #     # return model_delete(request, BaseInfo)
    #     # from_data = parse_data(request)
    #     from_data = request.query_params  # 返回QueryDict类型
    #     # print(params.get("user_id"))
    #     if not 'id' in from_data.keys() and not 'user_id' in from_data.keys():
    #         return util_response('', 7557, "用户ID不能为空")
    #     if from_data.get("id", None):
    #         user_id = from_data['id']
    #     else:
    #         user_id = from_data['user_id']
    #
    #     res = BaseInfo.objects.filter(id=user_id)
    #     if not res:
    #         return util_response('', 7557, "数据不存在")
    #
    #     detailinfo = DetailInfo.objects.filter(user_id=user_id).first()
    #     if detailinfo:
    #         DetailInfo.objects.filter(user_id=user_id).delete()
    #     res.delete()
    #     return util_response()
    @user_authentication_force_wrapper
    @request_params_wrapper
    def delete(self, *args, user_info=None, request_params=None, **kwargs):
        if request_params is None:
            request_params = {}
        if user_info is None:
            user_info = {}

        user_id = request_params.pop("user_id", None) or user_info.get("user_id")  # 没有传则修改当前的用户的信息

        res = BaseInfo.objects.filter(id=user_id)
        if not res:
            return util_response('', 7557, "数据不存在")
        res.update(**{"is_delete": 1})
        # 删除所有单点登录信息
        UserSsoToUser.objects.filter(
            user_id=user_id,
        ).update(is_delete=1)
        return util_response()


class MyApiError(Exception):
    def __init__(self, message, err_code=4010):
        self.msg = message
        self.err = err_code

    def __str__(self):
        # repr()将对象转化为供解释器读取的形式。可省略
        return repr(self.msg)
