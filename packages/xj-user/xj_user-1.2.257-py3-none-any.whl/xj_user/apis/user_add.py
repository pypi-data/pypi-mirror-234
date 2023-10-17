# _*_coding:utf-8_*_
import sys

from django.views.decorators.http import require_http_methods
from rest_framework.views import APIView

from ..services.user_relate_service import UserRelateToUserService

if 'xj_role' in sys.modules:
    from xj_role.services.role_service import RoleService
    from xj_role.services.user_group_service import UserGroupService
from ..models import Platform, PlatformsToUsers
from ..services.user_detail_info_service import DetailInfoService
from ..services.user_service import UserService
from ..utils.custom_tool import request_params_wrapper, format_params_handle
from ..utils.model_handle import util_response
from ..utils.user_wrapper import user_authentication_force_wrapper


# 管理员添加用户
class UserAdd(APIView):

    @require_http_methods(['POST'])
    @user_authentication_force_wrapper
    @request_params_wrapper
    def add(self, *args, request_params=None, **kwargs):
        if request_params is None:
            request_params = {}
        if not request_params.get("platform_code", None):
            return util_response(err=1001, msg="平台码不能为空")
        platform_set = Platform.objects.filter(platform_code=request_params.get("platform_code", None)).first()
        if not platform_set:
            return util_response(err=1001, msg="平台不存在")
        # 获取角色和部门的id列表
        user_role_list = request_params.pop('user_role_list', None)
        user_group_list = request_params.pop('user_group_list', None)
        belong_list = request_params.pop('belong_list', None)

        # TODO 针对劳务通系统做的个人用户绑定企业用户功能
        relate_key = request_params.pop('relate_key', None)

        # 进行用户添加
        data, err = UserService.user_add(request_params)
        if err:
            return util_response(err=1001, msg=err)

        # 联动添加用户详细信息
        user_id = data.get("user_id")
        if user_id:
            detail_params = format_params_handle(
                param_dict=request_params,
                remove_filed_list=["account", "password", "full_name", "nickname"]
            )
            detail_params.setdefault("user_id", user_id)
            detail_params.setdefault("real_name", "系统分配用户")
            detail_add_data, err = DetailInfoService.create_or_update_detail(detail_params)

        platforms_users = PlatformsToUsers.objects.create(**{
            "platform_id": platform_set.id,
            "user_id": user_id
        })
        if not platforms_users:
            return "平台写入失败"

        # 绑定用户的角色和组织
        if user_group_list and user_id:
            UserGroupService.user_bind_groups(user_id, user_group_list)
        if user_role_list and user_id:
            RoleService.bind_user_role(user_id, user_role_list)

        # TODO 针对劳务通系统做的个人用户绑定企业用户功能
        if belong_list and user_id:
            UserRelateToUserService.laowu_bind_bxtx_relate(
                {
                    "user_id_list": belong_list,
                    "with_user_id": user_id,
                    "relate_key": relate_key
                })

        return util_response(data=data)
