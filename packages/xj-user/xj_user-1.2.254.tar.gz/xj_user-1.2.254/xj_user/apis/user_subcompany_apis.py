# _*_coding:utf-8_*_
from rest_framework.views import APIView

from ..services.user_subcompany_service import UserSubCompanyService
from ..utils.custom_tool import request_params_wrapper, format_params_handle
from ..utils.model_handle import util_response
from ..utils.user_wrapper import user_authentication_force_wrapper


# 分子公司管理
class UserSubCompanyAPIView(APIView):
    # 分子公司列表
    @user_authentication_force_wrapper
    @request_params_wrapper
    def get(self, *args, request_params=None, detail_id=None, **kwargs):
        data, err = UserSubCompanyService.get_sub_company(params=request_params, detail_id=detail_id)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    # 添加分子公司
    @user_authentication_force_wrapper
    @request_params_wrapper
    def post(self, *args, request_params=None, user_info, **kwargs):
        data, err = UserSubCompanyService.add(params=request_params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    # # 修改分子公司
    @user_authentication_force_wrapper
    @request_params_wrapper
    def put(self, *args, request_params=None, detail_id=None, **kwargs):
        pk = request_params.pop("id", None) or request_params.pop("pk", None) or detail_id
        data, err = UserSubCompanyService.edit(pk=pk, update_params=request_params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    # 删除分子公司
    @user_authentication_force_wrapper
    @request_params_wrapper
    def delete(self, *args, request_params=None, detail_id=None, **kwargs):
        pk = request_params.pop("id", None) or kwargs.pop("pk", None) or detail_id
        data, err = UserSubCompanyService.delete(pk=pk)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)
