# encoding: utf-8
"""
@project: djangoModel->user_bank_service
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 用户设备信息
@created_time: 2023/6/8 16:20
"""
from django.core.paginator import Paginator, EmptyPage

from xj_user.models import UserDevice
from ..utils.custom_tool import format_params_handle, force_transform_type


class UserDeviceService():
    @staticmethod
    def get_devices(params=None, pk=None, allow_user_list=None, only_first=False, **kwargs):
        allow_user_list = [i for i in allow_user_list if i] if allow_user_list else None
        # 查看详情
        pk, err = force_transform_type(variable=pk, var_type="int")
        if pk:
            return UserDevice.objects.filter(id=pk).values().first(), None
        else:
            # 参数搜索接口
            params, err = force_transform_type(variable=params, var_type="dict", default={})
            kwargs, err = force_transform_type(variable=kwargs, var_type="dict", default={})
            params.update(kwargs)

            # 分页参数
            size, err = force_transform_type(variable=params.get("size"), var_type="int", default=10)
            page, err = force_transform_type(variable=params.get("page"), var_type="int", default=1)

            # 过滤字段
            filter_params = format_params_handle(
                param_dict=params,
                filter_filed_list=[
                    "id", "id_list|list_int", "user_id|int", "user_id_list|list_int", "client_id", "system", "ip", "device_model",
                ],
                alias_dict={"id_list": "id__in", "user_id_list": "user_id__in"}
            )

            # 排序字段
            sort = params.get("sort")
            sort = sort if sort in ["id", "-id", "update_time", "create_time", "-update_time", "-create_time"] else "-id"

            # 构建ORM进行查询
            user_device_set = UserDevice.objects
            if not allow_user_list is None and isinstance(allow_user_list, list):  # 筛选可以访问的列表
                user_device_set = user_device_set.filter(id__in=allow_user_list)
            cards_obj = user_device_set.filter(**filter_params).order_by(sort).values()
            count = cards_obj.count()

            if only_first:
                return cards_obj.first(), None

            try:
                page_set = Paginator(cards_obj, size).get_page(page)
            except EmptyPage:
                return {'count': count, "page": page, "size": size, "list": []}, None

            return {'count': count, "page": page, "size": size, "list": list(page_set.object_list)}, None

    @staticmethod
    def create_or_update(params: dict = None):
        if params is None:
            params = {}
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=["user_id|int", "client_id", "system", "ip", "device_model"]
        )

        user_id = params.get("user_id")
        if not user_id:
            return None, "参数错误，用户ID必传"

        user_device_obj = UserDevice.objects.filter(user_id=user_id)
        try:
            if not user_device_obj.first():
                device_set = UserDevice.objects.create(**params)
                return {"id": device_set.id}, None
            else:
                user_device_obj.update(**params)
                return {"id": user_id}, None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def delete(pk=None):
        if not pk:
            return None, "参数错误"
        device_obj = UserDevice.objects.filter(id=pk)
        if not device_obj:
            return None, None
        try:
            device_obj.delete()
        except Exception as e:
            return None, "删除异常:" + str(e)
        return None, None

    @staticmethod
    def add(params=None):
        if params is None:
            params = {}
        filter_params = format_params_handle(
            param_dict=params,
            filter_filed_list=["user_id|int", "client_id", "system", "ip", "device_model"]
        )
        try:
            device_set = UserDevice.objects.create(**filter_params)
            return {"id": device_set.id}, None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def edit(pk=None, update_params=None):
        if update_params is None:
            update_params = {}
        filter_params = format_params_handle(
            param_dict=update_params,
            filter_filed_list=["user_id|int", "client_id", "system", "ip", "device_model"]
        )
        if not pk or not filter_params:
            return None, "没有可修改的数据"
        try:
            device_obj = UserDevice.objects.filter(id=pk)
            if not device_obj:
                return None, "没有可修改的数据"
            device_obj.update(**filter_params)

            return None, None
        except Exception as e:
            return None, str(e)
