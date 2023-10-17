# encoding: utf-8

from django.core.paginator import Paginator, EmptyPage
from xj_user.models import UserSubCompany
from django.db.models import Q
from ..utils.custom_tool import format_params_handle, force_transform_type


class UserSubCompanyService():
    @staticmethod
    def get_sub_company(params=None, detail_id=None, allow_user_list=None):
        allow_user_list = [i for i in allow_user_list if i] if allow_user_list else None
        # 查看详情
        detail_id, err = force_transform_type(variable=detail_id, var_type="int")
        if detail_id:
            return UserSubCompany.objects.filter(id=detail_id).values().first(), None
        else:
            params, err = force_transform_type(variable=params, var_type="dict", default={})
            size, err = force_transform_type(variable=params.get("size"), var_type="int", default=10)
            page, err = force_transform_type(variable=params.get("page"), var_type="int", default=1)
            sort = params.get("sort")
            filter_params = format_params_handle(
                param_dict=params,
                filter_filed_list=["id", "name", "updated_time"],
                split_list=[],
                alias_dict={},
            )
            # 排序字段
            allow_sort = ["id", "-id", "sort", "-sort"]
            sort = sort if sort in allow_sort else "-id"
            user_sub_company_set = UserSubCompany.objects
            if not allow_user_list is None and isinstance(allow_user_list, list):  # 筛选可以访问的列表
                user_sub_company_set = user_sub_company_set.filter(id__in=allow_user_list)
            # 构建模糊查询参数集并删除 filter_params 中包含的参数
            contains_keys = ["name"]
            contains_params = {}
            contains_query = Q()
            for key in contains_keys:
                if key in filter_params:
                    contains_params[key] = filter_params.pop(key)
                    contains_query |= Q(**{key + '__icontains': contains_params[key]})
            # 去掉 filter_params 中包含的参数
            filter_params = {key: value for key, value in filter_params.items() if key not in contains_keys}
            companies_obj = user_sub_company_set.filter(contains_query).filter(**filter_params).order_by(sort).values()
            count = companies_obj.count()
            formatted_companies = []
            for company in companies_obj:
                company['created_time'] = company['created_time'].strftime('%Y-%m-%d %H:%M:%S')
                company['updated_time'] = company['updated_time'].strftime('%Y-%m-%d %H:%M:%S')
                formatted_companies.append(company)
            try:
                page_set = Paginator(formatted_companies, size).get_page(page)
            except EmptyPage:
                return {'count': count, "page": page, "size": size, "list": []}, None

            return {'count': count, "page": page, "size": size, "list": list(page_set.object_list)}, None

    @staticmethod
    def add(params=None):
        if params is None:
            params = {}
        filter_params = format_params_handle(
            param_dict=params,
            filter_filed_list=["name", "sort"]
        )
        try:
            company_obj = UserSubCompany.objects.create(**filter_params)
            return {"id": company_obj.id}, None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def edit(pk=None, update_params=None):
        if update_params is None:
            update_params = {}
        filter_params = format_params_handle(
            param_dict=update_params,
            filter_filed_list=["name", "sort"]
        )
        if not pk or not filter_params:
            return None, "没有可修改的数据"
        try:
            cards_obj = UserSubCompany.objects.filter(id=pk)
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
        cards_obj = UserSubCompany.objects.filter(id=pk)
        if not cards_obj:
            return None, None
        try:
            cards_obj.delete()
        except Exception as e:
            return None, "删除异常:" + str(e)
        return None, None
