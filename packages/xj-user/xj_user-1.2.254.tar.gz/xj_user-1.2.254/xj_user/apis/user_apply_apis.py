# encoding: utf-8
"""
@project: djangoModel->user_apply_apis
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 用户申请APIS
@created_time: 2023/9/7 13:54
"""
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from ..services.user_apply_services import UserApplyServices
from ..utils.custom_response import util_response
from ..utils.custom_tool import request_params_wrapper
from ..utils.user_wrapper import user_authentication_force_wrapper, user_authentication_wrapper


class UserApplyApis(APIView):

    @api_view(["GET"])
    @request_params_wrapper
    @user_authentication_wrapper
    def apply_type_list(self, *args, request_params, user_info, **kwargs):
        """审批类型列表"""
        data, err = UserApplyServices.apply_type_list()
        return util_response(data=data)

    @api_view(["GET", "POST", "PUT"])
    @request_params_wrapper
    @user_authentication_force_wrapper
    def add_user_apply(self, *args, request_params, user_info, **kwargs):
        request_params.setdefault("user_id", user_info.get("user_id"))
        data, err = UserApplyServices.add_apply_record(request_params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @api_view(["GET", "POST", "PUT"])
    @request_params_wrapper
    @user_authentication_force_wrapper
    def agree_user_apply(self, *args, request_params, user_info, **kwargs):
        request_params.setdefault("verify_user_id", user_info.get("user_id"))
        request_params.setdefault("result", "VERIFY_PASS")
        pk = request_params.get("pk")
        data, err = UserApplyServices.edit_apply_record(request_params, pk=pk)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @api_view(["GET", "POST", "PUT"])
    @request_params_wrapper
    @user_authentication_force_wrapper
    def disagree_user_apply(self, *args, request_params, user_info, **kwargs):
        pk = request_params.get("pk")
        request_params.setdefault("verify_user_id", user_info.get("user_id"))
        request_params.setdefault("result", "VERIFY_REJECT")
        reject_reason = request_params.get("reject_reason")
        if not reject_reason:
            return util_response(err=1000, msg="决绝理由不能为空")

        data, err = UserApplyServices.edit_apply_record(request_params, pk=pk)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @api_view(["GET", "POST", "PUT"])
    @request_params_wrapper
    @user_authentication_force_wrapper
    def user_apply_list(self, *args, request_params, user_info, **kwargs):
        request_params.setdefault("user_id", user_info.get("user_id"))
        data, err = UserApplyServices.apply_record_list(request_params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @api_view(["GET", "POST", "PUT"])
    @request_params_wrapper
    @user_authentication_force_wrapper
    def user_apply_statistics(self, *args, request_params, user_info, **kwargs):
        request_params.setdefault("user_id", user_info.get("user_id"))
        data, err = UserApplyServices.apply_record_agg(request_params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)
