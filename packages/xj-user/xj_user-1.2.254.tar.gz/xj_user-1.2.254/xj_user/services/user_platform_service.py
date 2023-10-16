# _*_coding:utf-8_*_
from logging import getLogger

from django.core.paginator import Paginator
from django.db.models import Q, F
from django.forms import model_to_dict

from ..models import Platform, PlatformsToUsers
from ..utils.custom_tool import format_params_handle, filter_result_field


class UserPlatformService:
    def __init__(self):
        pass

    # 检测账户
    @staticmethod
    def get_platform_info(platform_name=None):
        if not platform_name:
            return None, '平台参数未传(platform_name)'

        platform_set = Platform.objects.filter(platform_name=platform_name).first()
        # print(">  get_platform_info platform_set:", platform_set, type(platform_set))
        if not platform_set:
            return None, '平台不存在'

        return model_to_dict(platform_set), None

        # 检测账户

    @staticmethod
    def payment_get_platform_info(platform_id=None, platform_code=None):
        if not platform_id and not platform_code:
            return None, '平台不能为空'
        if platform_id:
            platform_set = Platform.objects.filter(platform_id=platform_id).first()
        elif platform_code:
            platform_set = Platform.objects.filter(platform_code=platform_code).first()
        # print(">  get_platform_info platform_set:", platform_set, type(platform_set))
        if not platform_set:
            return None, '平台不存在'

        return model_to_dict(platform_set), None

    @staticmethod
    def get_platform_info_by_user_id(user_id=None):
        """
        通过用户ID检索平台信息（获取用户的平台信息）
        :param user_id:
        :return:data ,err
        """
        if not user_id:
            return None, 'user_id必传'

        platform_set = PlatformsToUsers.objects.annotate(
            user_platform_name=F("platform__platform_name"),
            user_platform_id=F("platform__platform_id"),
            user_platform_code=F("platform__platform_code"),
        ).filter(platform_user_id=user_id)
        if not platform_set:
            return None, '平台不存在'
        platform_res = filter_result_field(
            result_list=platform_set.to_json(),
            alias_dict={
                "user_platform_id": "platform_id",
                "user_platform_name": "platform_name",
                "user_platform_code": "platform_code",
            }
        )
        return platform_res, None

    @staticmethod
    def list(params={}, need_pagination=1, id_list=None):
        size = params.pop('size', 10)
        page = params.pop('page', 1)
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=["platform_id", "platform_name", "platform_code"],
            alias_dict={"platform_name": "platform_name__contains"}
        )
        Platform_set = Platform.objects
        if not id_list:
            return [], None
        Platform_set = Platform_set.filter(platform_id__in=id_list)
        try:
            fetch_obj = Platform_set.filter(**params).values()
            if not need_pagination:
                return list(fetch_obj), None
            count = fetch_obj.count()

            paginator = Paginator(fetch_obj, size)
            page_obj = paginator.page(page)
            data = {'total': count, "size": size, 'page': page, 'list': list(page_obj.object_list)}

            return data, None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def edit(params):
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=["platform_id", "platform_name", "platform_code", ],
        )

        platform_id = params.pop("platform_id", None)
        if not params or not platform_id:
            return None, "无效参数"

        query_obj = Platform.objects.filter(platform_id=platform_id)
        if not query_obj.first():
            return None, "修改参数未生效"

        try:
            query_obj.update(**params)
        except Exception as e:
            return None, "修改异常:" + str(e)
        return None, None

    @staticmethod
    def delete(params):
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=["platform_id", "platform_name", "platform_code", ],
        )
        if not params:
            return None, "无效参数"

        query_obj = Platform.objects.filter(**params)
        if not query_obj:
            return None, None

        try:
            query_obj.delete()
        except Exception as e:
            return None, "删除异常:" + str(e)
        return None, None

    @staticmethod
    def add(params):
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=["platform_id", "platform_name", "platform_code"],
        )

        if not params.get("platform_id") or not params.get("platform_name") or not params.get("platform_code"):
            return None, "对不起，参数错误"

        filter_obj = Platform.objects.filter(
            Q(platform_id=params.get("platform_id")) | Q(platform_name=params.get("platform_name")) | Q(
                platform_code=params.get("platform_code"))
        ).first()
        if filter_obj:
            return None, "对不起，平台ID、平台名称、平台编码必须是唯一的"

        try:
            Platform.objects.create(**params)
        except Exception as e:
            return None, str(e)

        return None, None

        # 检测账户
