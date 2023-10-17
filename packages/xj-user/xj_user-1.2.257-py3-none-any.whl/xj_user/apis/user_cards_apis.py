# _*_coding:utf-8_*_
from rest_framework.views import APIView

from ..services.user_bank_service import UserBankCardsService
from ..services.user_service import UserService
from ..utils.custom_tool import request_params_wrapper, format_params_handle
from ..utils.model_handle import util_response
from ..utils.user_wrapper import user_authentication_force_wrapper
from ..utils.utility_method import extract_values, replace_key_in_dict_replacement_dicts


# 银行卡管理
class UserBankAPIView(APIView):
    # 卡片列表
    @request_params_wrapper
    def get(self, *args, request_params=None, detail_id=None, **kwargs):
        # ================== 用户id列表反查询报名 start===============================
        account_params = format_params_handle(
            param_dict=request_params,
            filter_filed_list=["user_name", 'real_name', 'nickname'],
            is_remove_empty=True
        )

        if account_params:
            account_ids, err = UserService.user_list(
                params=account_params)
            if not err:
                request_params["user_id_list"] = extract_values(account_ids['list'], 'user_id')

            if isinstance(request_params.get("user_id_list"), list) and len(
                    request_params["user_id_list"]) == 0:
                request_params["user_id_list"] = [0]
        # ================== 用户id列表反查询报名 end ===============================

        data, err = UserBankCardsService.get_bank_card(params=request_params, detail_id=detail_id)
        print(456)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    # 添加卡片
    @user_authentication_force_wrapper
    @request_params_wrapper
    def post(self, *args, request_params=None, user_info, **kwargs):
        request_params.setdefault("user_id", user_info.get("user_id"))
        data, err = UserBankCardsService.add(params=request_params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response()

    # # 修改卡片
    @user_authentication_force_wrapper
    @request_params_wrapper
    def put(self, *args, request_params=None, **kwargs):
        pk = request_params.pop("id", None) or request_params.pop("pk", None)
        data, err = UserBankCardsService.edit(pk=pk, update_params=request_params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    # 删除卡片
    @user_authentication_force_wrapper
    @request_params_wrapper
    def delete(self, *args, request_params=None, **kwargs):
        pk = request_params.pop("id", None) or kwargs.pop("pk", None)
        data, err = UserBankCardsService.delete(pk=pk)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)
