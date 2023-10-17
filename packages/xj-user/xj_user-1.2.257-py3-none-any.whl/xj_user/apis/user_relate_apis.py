# encoding: utf-8
"""
@project: djangoModel->user_relate_apis
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 用户的关系方法们
@created_time: 2022/12/13 16:42
"""
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from ..services.user_relate_service import UserRelateTypeService, UserRelateToUserService
from ..utils.custom_response import util_response
from ..utils.custom_tool import request_params_wrapper
from ..utils.user_wrapper import user_authentication_force_wrapper


class UserRelateTypeApis(APIView):
    # 关系列表
    @request_params_wrapper
    def get(self, *args, request_params=None, **kwargs):
        data, err = UserRelateTypeService.list(params=request_params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    # 添加关系
    @request_params_wrapper
    def post(self, *args, request_params=None, **kwargs):
        data, err = UserRelateTypeService.add(params=request_params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    # 修改关系
    @request_params_wrapper
    def put(self, *args, request_params=None, **kwargs):
        pk = request_params.pop("id", None) or request_params.pop("pk", None)
        data, err = UserRelateTypeService.edit(pk=pk, update_params=request_params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    # 删除关系
    @request_params_wrapper
    def delete(self, *args, request_params=None, **kwargs):
        pk = request_params.pop("id", None) or request_params.pop("pk", None)
        data, err = UserRelateTypeService.delete(pk=pk)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)


class UserRelateToUserApis(APIView):
    # 关系列表
    @request_params_wrapper
    def get(self, *args, request_params=None, **kwargs):
        data, err = UserRelateToUserService.list(
            params=request_params,
            filter_fields=request_params.get("filter_fields", None)
        )
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    # 添加关系
    @request_params_wrapper
    def post(self, *args, request_params=None, **kwargs):
        data, err = UserRelateToUserService.add(params=request_params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response()

    # # 修改关系
    # @request_params_wrapper
    # def put(self, *args, request_params=None, **kwargs):
    #     pk = request_params.pop("id", None) or request_params.pop("pk", None)
    #     data, err = UserRelateToUserService.edit(pk=pk, params=request_params)
    #     if err:
    #         return util_response(err=1000, msg=err)
    #     return util_response(data=data)

    # 删除关系
    @request_params_wrapper
    def delete(self, *args, request_params=None, **kwargs):
        pk = request_params.pop("id", None) or request_params.pop("pk", None)
        data, err = UserRelateToUserService.delete(pk=pk)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    # 绑定用户关系
    @api_view(["GET", "POST"])
    @user_authentication_force_wrapper
    @request_params_wrapper
    def bind_bxtx_relate(self, *args, request_params=None, user_info=None, **kwargs):
        data, err = UserRelateToUserService.bind_bxtx_relate(params=request_params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

        # 绑定用户关系

    @api_view(["GET", "POST"])
    @request_params_wrapper
    def laowu_bind_bxtx_relate(self, *args, request_params=None, user_info=None, **kwargs):
        data, err = UserRelateToUserService.laowu_bind_bxtx_relate(params=request_params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    # 绑定用户关系
    @api_view(["GET", "POST"])
    @user_authentication_force_wrapper
    @request_params_wrapper
    def bxtx_relate_user(self, *args, request_params=None, user_info=None, **kwargs):
        request_params.setdefault("user_id", user_info.get("user_id"))
        data, err = UserRelateToUserService.bxtx_relate_user(params=request_params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    # 用戶分銷關係
    @api_view(["GET"])
    @user_authentication_force_wrapper
    @request_params_wrapper
    def distribution_relate(self, *args, request_params=None, user_info=None, **kwargs):
        request_params.setdefault("user_id", user_info.get("user_id"))
        data, err = UserRelateToUserService.distribution_relate(params=request_params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

        # 用戶分銷關係

    @api_view(["GET"])
    # @user_authentication_force_wrapper
    @request_params_wrapper
    def relate_user_tree(self, *args, request_params=None, user_info=None, **kwargs):
        # request_params.setdefault("user_id", user_info.get("user_id"))
        data, err = UserRelateToUserService.group_tree_user(params=request_params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)
