# encoding: utf-8
"""
@project: djangoModel->user_bank_service
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 用户银行卡服务
@created_time: 2023/6/8 16:20
"""
from django.core.paginator import Paginator, EmptyPage
from django.db.models import F
from xj_user.models import UserBankCards
from ..utils.custom_tool import format_params_handle, force_transform_type


class UserBankCardsService():
    @staticmethod
    def get_bank_card(params=None, detail_id=None, allow_user_list=None):
        allow_user_list = [i for i in allow_user_list if i] if allow_user_list else None
        # 查看详情
        detail_id, err = force_transform_type(variable=detail_id, var_type="int")
        if detail_id:
            return UserBankCards.objects.filter(id=detail_id).values().first(), None
        else:
            params, err = force_transform_type(variable=params, var_type="dict", default={})
            size, err = force_transform_type(variable=params.get("size"), var_type="int", default=10)
            page, err = force_transform_type(variable=params.get("page"), var_type="int", default=1)
            sort = params.get("sort")
            filter_params = format_params_handle(
                param_dict=params,
                filter_filed_list=["id", "user_id", "bank_card_num", "open_account_bank", "opening_branch",
                                   "is_default", "user_id_list"],
                split_list=["user_id_list"],
                alias_dict={"user_id_list": "user_id__in"},
            )
            # 排序字段
            allow_sort = ["id", "-id", "sort", "-sort"]
            sort = sort if sort in allow_sort else "-id"
            user_bank_card_set = UserBankCards.objects
            if not allow_user_list is None and isinstance(allow_user_list, list):  # 筛选可以访问的列表
                user_bank_card_set = user_bank_card_set.filter(id__in=allow_user_list)
            cards_obj = user_bank_card_set.filter(**filter_params).annotate(
                user_name=F("user__user_name"),
                full_name=F("user__full_name"),
                nickname=F("user__nickname"), ).order_by(sort).values()
            count = cards_obj.count()
            try:
                page_set = Paginator(cards_obj, size).get_page(page)
            except EmptyPage:
                return {'count': count, "page": page, "size": size, "list": []}, None

            return {'count': count, "page": page, "size": size, "list": list(page_set.object_list)}, None

    @staticmethod
    def add(params=None):
        if params is None:
            params = {}
        filter_params = format_params_handle(
            param_dict=params,
            filter_filed_list=["user_id|int", "bank_card_num", "open_account_bank", "opening_branch", "is_default|int",
                               "remark",
                               "ext|dict"]
        )
        try:
            cards_obj = UserBankCards.objects.create(**filter_params)
            return {"id": cards_obj.id}, None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def edit(pk=None, update_params=None):
        if update_params is None:
            update_params = {}
        filter_params = format_params_handle(
            param_dict=update_params,
            filter_filed_list=["bank_card_num", "open_account_bank", "opening_branch", "is_default|int", "remark",
                               "ext|dict"]
        )
        if not pk or not filter_params:
            return None, "没有可修改的数据"
        try:
            cards_obj = UserBankCards.objects.filter(id=pk)
            if not cards_obj:
                return None, "没有可修改的数据"
            cards_obj.update(**filter_params)

            return None, None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def delete(pk=None):
        if not pk:
            return None, "参数错误"
        cards_obj = UserBankCards.objects.filter(id=pk)
        if not cards_obj:
            return None, None
        try:
            cards_obj.delete()
        except Exception as e:
            return None, "删除异常:" + str(e)
        return None, None
