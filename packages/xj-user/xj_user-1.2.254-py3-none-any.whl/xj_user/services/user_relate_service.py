# encoding: utf-8
"""
@project: djangoModel->user_relate_service
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 用户关系服务
@created_time: 2022/12/13 16:45
"""
from decimal import Decimal
import sys

from django.core.paginator import Paginator, EmptyPage
from django.db.models import F, Q, Case, When, Value, CharField, OuterRef
from orator import DatabaseManager

from config.config import JConfig

# from tz_sys_biaoxing.utils.j_recur import JRecur
if 'xj_role' in sys.modules:
    from xj_role.services.role_service import RoleService
from ..models import UserRelateType, UserRelateToUser, BaseInfo, DetailInfo
from ..services.user_detail_info_service import DetailInfoService
# 用户关系类型服务
from ..utils.custom_tool import format_params_handle, force_transform_type, filter_fields_handler, dynamic_load_class
from ..utils.utility_method import generate_query_string, parse_integers

config = JConfig()
db_config = {
    config.get('main', 'driver', "mysql"): {
        'driver': config.get('main', 'driver', "mysql"),
        'host': config.get('main', 'mysql_host', "127.0.0.1"),
        'database': config.get('main', 'mysql_database', ""),
        'user': config.get('main', 'mysql_user', "root"),
        'password': config.get('main', 'mysql_password', "123456"),
        "port": config.getint('main', 'mysql_port', "3306")
    }
}
db = DatabaseManager(db_config)


class UserRelateTypeService():
    @staticmethod
    def list(params=None):
        if params is None:
            params = {}
        size = params.get("size", 10)
        page = params.get("page", 20)
        filter_params = format_params_handle(
            param_dict=params,
            filter_filed_list=["id", "relate_key", "relate_name", ]
        )
        relate_obj = UserRelateType.objects.filter(**filter_params).values()
        count = relate_obj.count()
        page_set = Paginator(relate_obj, size).get_page(page)
        return {'count': count, "page": page, "size": size, "list": list(page_set.object_list)}, None

    @staticmethod
    def add(params=None):
        if params is None:
            params = {}
        filter_params = format_params_handle(
            param_dict=params,
            filter_filed_list=["relate_key", "relate_name", "description", "is_multipeople"]
        )
        try:
            relate_obj = UserRelateType.objects.create(**filter_params)
            return {"id": relate_obj.id}, None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def edit(pk=None, update_params=None):
        if update_params is None:
            update_params = {}
        filter_params = format_params_handle(
            param_dict=update_params,
            filter_filed_list=["relate_key", "relate_name", "description", "is_multipeople"]
        )
        if not pk or not filter_params:
            return None, "没有可修改的数据"
        try:
            relate_obj = UserRelateType.objects.filter(id=pk)
            if not relate_obj:
                return None, "没有可修改的数据"
            relate_obj.update(**filter_params)

            return None, None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def delete(pk=None):
        if not pk:
            return None, "参数错误"
        relate_obj = UserRelateType.objects.filter(id=pk)
        if not relate_obj:
            return None, None
        try:
            relate_obj.delete()
        except Exception as e:
            return None, "删除异常:" + str(e)
        return None, None


# 用户关系映射服务
class UserRelateToUserService():
    @staticmethod
    def list(params=None, filter_fields=None, only_first=False, **kwargs):
        """
        查询用户关系映射
        :param params: 参数
        :param filter_fields: 过滤字段
        :param only_first: 仅仅查询第一条
        """
        # ------------------------- section 参数处理 start ------------------------------------
        params, err = force_transform_type(variable=params, var_type="dict", default={})
        size, err = force_transform_type(variable=params.get("size"), var_type="int", default=10)
        page, err = force_transform_type(variable=params.get("page"), var_type="int", default=1)
        need_pagination, err = force_transform_type(variable=params.get("need_pagination"), var_type="bool",
                                                    default=True)
        sort = params.get("sort")
        sort = sort if sort and sort in ["created_time", "-created_time", "id", "-id"] else "-created_time"
        default_field_list = [
            "user_id", "with_user_id", "user_relate_type_id", "relate_key", "relate_type_name",
            "user_name", "full_name", "nickname", "with_user_name", "with_full_name", "with_nickname",
            "created_time"
        ]
        filter_fields = filter_fields_handler(
            input_field_expression=filter_fields,
            default_field_list=default_field_list,
            all_field_list=default_field_list + ["user_phone", "with_user_phone"]
        )

        # 真名查询
        if params.get("real_name"):
            user_id_list = list(
                DetailInfo.objects.filter(real_name__contains=params.get("real_name")).values("user_id"))
            params.setdefault("user_id_list", [i["user_id"] for i in user_id_list])

        if params.get("with_real_name"):
            user_id_list = list(
                DetailInfo.objects.filter(real_name__contains=params.get("with_real_name")).values("user_id"))
            params.setdefault("with_user_id_list", [i["user_id"] for i in user_id_list])

        filter_params = format_params_handle(
            param_dict=params,
            filter_filed_list=[
                "user_id|int", "user_id_list", "with_user_id_list", "with_user_id|int", "user_relate_type_id|int",
                "relate_key",
                "user_name", "full_name", "user_phone", "with_user_phone", "nickname", "with_user_name",
                "with_full_name", "with_nickname",
                "created_time_start", "created_time_end"
            ],
            alias_dict={
                "user_id_list": "user_id__in", "with_user_id_list": "with_user_id__in",
                "created_time_start": "created_time__gte", "created_time_end": "created_time__lte"
            },
            split_list=["user_id_list", "with_user_id_list"]
        )
        # ------------------------- section 参数处理 end   ------------------------------------

        # ------------------------- section 构建ORM start ------------------------------------
        contains_keys = ["user_phone", "with_user_name", "full_name"]
        contains_params = {}
        contains_query = Q()
        for key in contains_keys:
            if key in filter_params:
                contains_params[key] = filter_params.pop(key)
                contains_query |= Q(**{key + '__icontains': contains_params[key]})
        # 去掉 filter_params 中包含的参数
        filter_params = {key: value for key, value in filter_params.items() if key not in contains_keys}
        relate_user_obj = UserRelateToUser.objects.extra(
            select={"created_time": 'DATE_FORMAT(created_time, "%%Y-%%m-%%d %%H:%%i:%%s")'}
        ).annotate(
            relate_key=F("user_relate_type__relate_key"),
            relate_type_name=F("user_relate_type__relate_name"),
            user_name=F("user__user_name"),
            user_phone=F("user__phone"),
            full_name=F("user__full_name"),
            nickname=F("user__nickname"),
            with_user_name=F("with_user__user_name"),
            with_user_phone=F("with_user__phone"),
            with_full_name=F("with_user__full_name"),
            with_nickname=F("with_user__nickname"),
        ).filter(user__is_delete=0, with_user__is_delete=0).order_by(sort).filter(contains_query).filter(
            **filter_params)
        # ------------------------- section 构建ORM end ------------------------------------

        # # ------------------------- section 追加字段 start ------------------------------------
        # # TODO 追加字段
        relate_user_obj = relate_user_obj.values(*filter_fields)
        # if "invite" in filter_params.get("relate_key", []):
        #     for obj in relate_user_obj:
        #         print(obj["user_id"])
        #         ancestor = UserRelateToUser.objects.filter(user__is_delete=0, with_user__is_delete=0,
        #                                                    with_user_id=obj["user_id"]).first()
        #         if ancestor:
        #             username = ancestor.with_user
        #             obj['ancestor_username'] = username
        # relate_user_obj_new.append(company)

        # ------------------------- section 追加字段 end ------------------------------------

        # ------------------------- section 构建返回体 start ------------------------------------
        # 单条返回
        if only_first:
            return relate_user_obj.first(), None

        # 列表返回
        total = relate_user_obj.count()
        if not need_pagination and total <= 200:
            return list(relate_user_obj), None

        # 分页返回
        else:
            try:
                page_set = Paginator(relate_user_obj, size).page(page)
            except EmptyPage:
                return {'total': total, "page": page, "size": size, "list": []}, None

            page_list = list(page_set.object_list)
            # 被邀请人的详细信息
            user_detail_list, err = DetailInfoService.get_list_detail(
                user_id_list=[i["user_id"] for i in page_list],
                filter_fields=["user_id", "avatar", "real_name", "nickname"]
            )
            user_detail_list = user_detail_list if user_detail_list else []
            user_detail_map = {i["user_id"]: i for i in user_detail_list}
            # 邀请人的详细信息
            with_user_detail_list, err = DetailInfoService.get_list_detail(
                user_id_list=[i["with_user_id"] for i in page_list],
                filter_fields=["user_id", "avatar", "real_name", "nickname"]
            )
            with_user_detail_list = with_user_detail_list if with_user_detail_list else []
            with_user_detail_map = {i["user_id"]: i for i in with_user_detail_list}
            # 详细信息拼接
            for j in page_list:
                j["avatar"] = user_detail_map.get(j["user_id"], {}).get("avatar", [])
                j["real_name"] = user_detail_map.get(j["user_id"], {}).get("real_name", "")
                j["nickname"] = user_detail_map.get(j["user_id"], {}).get("nickname", "")

                j["with_avatar"] = with_user_detail_map.get(j["with_user_id"], {}).get("avatar", [])
                j["with_real_name"] = with_user_detail_map.get(j["with_user_id"], {}).get("real_name", "")
                j["with_nickname"] = with_user_detail_map.get(j["with_user_id"], {}).get("nickname", "")
                if "invite" in filter_params.get("relate_key", []):
                    #  判断该用户是否是业务人员
                    role_info, err = RoleService.get_role_list(params={"user_id": j["user_id"]}, only_first=True)
                    is_salesperson = False
                    j['sale_username'] = ""
                    if role_info and role_info.get("role_key") == "BID-SALESMAN":
                        is_salesperson = True
                    if is_salesperson:
                        ancestor = UserRelateToUser.objects.filter(user__is_delete=0, with_user__is_delete=0,
                                                                   with_user_id=j["user_id"]).first()
                        if ancestor:
                            j['sale_username'] = ancestor.with_user.user_name if ancestor.with_user.user_name else ""

            return {'total': total, "page": page, "size": size, "list": list(page_set.object_list)}, None
        # ------------------------- section 构建返回体 end   ------------------------------------

    @staticmethod
    def add(params: dict = None, **kwargs):
        params, is_pass = force_transform_type(variable=params, var_type="dict", default={})
        kwargs, is_pass = force_transform_type(variable=kwargs, var_type="dict", default={})
        params.update(kwargs)

        # ------------------- section 获取关系类型 start ---------------------------
        relate_key = params.get("user_relate_type_value", params.get("relate_key"))
        if relate_key:
            user_relate_type = UserRelateType.objects.filter(relate_key=relate_key).values().first()
        else:
            user_relate_type = UserRelateType.objects.filter(id=params.get("user_relate_type_id")).values().first()
        if not user_relate_type:
            return None, "不是有效的关系类型"
        params.setdefault("user_relate_type_id", user_relate_type.get("id"))
        # ------------------- section 获取关系类型 end   ---------------------------

        # ------------------- section 过滤字段,并校验合法性 start ---------------------------
        # 参数处理
        filter_params = format_params_handle(
            param_dict=params,
            filter_filed_list=["user", "user_id", "with_user", "with_user_id", "user_relate_type",
                               "user_relate_type_id"],
            alias_dict={"user": 'user_id', "with_user": "with_user_id", "user_relate_type": "user_relate_type_id"}
        )
        if filter_params.get("user_id", None) is None or filter_params.get("with_user_id",
                                                                           None) is None or filter_params.get(
            "user_relate_type_id", None) is None:
            return None, "参数错误"
        # ------------------- section 过滤字段,并校验合法性 end   ---------------------------

        # ------------------- section 判断是否可以重复绑定 start ---------------------------
        if user_relate_type.get("is_multipeople"):
            # 检查是否已经绑定过
            relate_user_obj = UserRelateToUser.objects.filter(
                user_id=filter_params['user_id'],
                with_user=filter_params['with_user_id'],
                user_relate_type_id=filter_params['user_relate_type_id']
            ).first()
        else:
            # 可多人绑定的用户关系
            relate_user_obj = UserRelateToUser.objects.filter(
                user_id=filter_params['user_id'],
                user_relate_type_id=filter_params['user_relate_type_id']
            ).first()
        if relate_user_obj:
            return None, "无法重复绑定，或者该关系类型不是多人绑定类型。"
        # ------------------- section 判断是否可以重复绑定 end   ---------------------------

        # ------------------- section IO操作 start ---------------------------
        try:
            relate_user_obj = UserRelateToUser.objects.create(**filter_params)
            return {"id": relate_user_obj.id}, None
        except Exception as e:
            return None, str(e)
        # ------------------- section IO操作 end   ---------------------------

    @staticmethod
    def edit(pk=None, params=None):
        if params is None:
            params = {}
        filter_params = format_params_handle(
            param_dict=params,
            filter_filed_list=["user", "user_id", "with_user", "with_user_id", "user_relate_type",
                               "user_relate_type_id"],
            alias_dict={"user": 'user_id', "with_user": "with_user_id", "user_relate_type": "user_relate_type_id"}
        )
        if not pk or not params:
            return None, "没有可修改的数据"

        try:
            relate_user_obj = UserRelateToUser.objects.filter(id=pk)
            if not relate_user_obj:
                return None, "没有可修改的数据"
            relate_user_obj.update(**filter_params)
            return None, None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def delete(pk=None):
        if not pk:
            return None, "参数错误"
        relate_user_obj = UserRelateToUser.objects.filter(id=pk)
        if not relate_user_obj:
            return None, None
        try:
            relate_user_obj.delete()
        except Exception as e:
            return None, "删除异常:" + str(e)
        return None, None

    @staticmethod
    def distribution_relate(*args, params: dict = None, **kwargs):
        """
        查詢三級分銷接口
        :param params: 参数
        """
        # ------------------------- section 参数处理 start ------------------------------------
        kwargs, err = force_transform_type(variable=kwargs, var_type="only_dict", default={})
        params, err = force_transform_type(variable=params, var_type="only_dict", default={})
        params.update(kwargs)

        with_user_id, err = force_transform_type(variable=params.get("with_user_id"), var_type="int")
        relate_key, err = force_transform_type(variable=params.get("relate_key"), var_type="str", default="invite")
        select_level, err = force_transform_type(variable=params.get("select_level"), var_type="str")

        select_level = select_level if select_level in ["all", "first", "second", "third"] else "all"
        if not with_user_id:
            return None, "不是一个有效的 邀请人ID"

        size, err = force_transform_type(variable=params.pop('size', 10), var_type="int", default=10)
        page, err = force_transform_type(variable=params.pop('page', 1), var_type="int", default=1)

        if params.get("real_name"):
            user_id_list = list(
                DetailInfo.objects.filter(real_name__contains=params.get("real_name")).values("user_id"))
            params.setdefault("user_id_list", [i["user_id"] for i in user_id_list])

        params = format_params_handle(
            param_dict=params,
            filter_filed_list=[
                "relate_key", "relate_type_name", "user_name", "user_phone", "full_name", "nickname",
                "with_user_name", "with_user_phone", "with_full_name", "with_nickname", "user_id_list"
            ],
            alias_dict={"user_id_list": "user_id__in"}
        )
        # ------------------------- section 参数处理 end   ------------------------------------

        # ------------------------- section 构建ORM start ------------------------------------
        # 找出第一級別用戶
        first_users = list(UserRelateToUser.objects.filter(
            with_user_id=with_user_id,
            user_relate_type__relate_key="invite"
        ).values("user_id").distinct().order_by("user_id"))
        first_users = [i["user_id"] for i in first_users]

        # 找出第二級別用戶
        second_users = list(UserRelateToUser.objects.filter(
            with_user_id__in=first_users,
            user_relate_type__relate_key=relate_key
        ).values("user_id").distinct().order_by("user_id"))
        second_users = [i["user_id"] for i in second_users]

        # 查詢
        relate_user_obj = UserRelateToUser.objects.extra(
            select={"created_time": 'DATE_FORMAT(created_time, "%%Y-%%m-%%d %%H:%%i:%%s")'}
        ).annotate(
            relate_key=F("user_relate_type__relate_key"),
            relate_type_name=F("user_relate_type__relate_name"),
            user_name=F("user__user_name"),
            user_phone=F("user__phone"),
            full_name=F("user__full_name"),
            nickname=F("user__nickname"),
            with_user_name=F("with_user__user_name"),
            with_user_phone=F("with_user__phone"),
            with_full_name=F("with_user__full_name"),
            with_nickname=F("with_user__nickname")
        ).filter(user_relate_type__relate_key=relate_key).filter(**params)

        # 分級別查詢
        if select_level == "first":
            relate_user_obj = relate_user_obj.filter(with_user_id=with_user_id)
        elif select_level == "second":
            relate_user_obj = relate_user_obj.filter(with_user_id__in=first_users)
        elif select_level == "third":
            relate_user_obj = relate_user_obj.filter(with_user_id__in=second_users)
        else:
            relate_user_obj = relate_user_obj.filter(with_user_id__in=second_users + first_users + [with_user_id])

        total = relate_user_obj.count()
        relate_user_list = list(relate_user_obj.values(
            "relate_key",
            "relate_type_name",
            "user_name",
            "user_phone",
            "full_name",
            "nickname",
            "with_user_name",
            "with_user_phone",
            "with_full_name",
            "with_nickname",
            "with_user_id",
            "user_id"
        ))
        # ------------------------- section 构建ORM end ------------------------------------

        # ------------------------- section 分页查询 start ------------------------------------
        try:
            page_list = Paginator(relate_user_list, size).page(page)
            page_list = page_list.object_list
        except EmptyPage as e:
            return {"page": page, "size": size, "total": total, "list": []}, None
        # ------------------------- section 分页查询 end   ------------------------------------

        # ------------------------- section 获取用戶信息 start ------------------------------------
        # 被邀请人的详细信息
        user_detail_list, err = DetailInfoService.get_list_detail(
            user_id_list=[i["user_id"] for i in page_list],
            filter_fields=["user_id", "avatar", "real_name", "nickname"]
        )
        user_detail_list = user_detail_list if user_detail_list else []
        user_detail_map = {i["user_id"]: i for i in user_detail_list}
        # 邀请人的详细信息
        with_user_detail_list, err = DetailInfoService.get_list_detail(
            user_id_list=[i["with_user_id"] for i in page_list],
            filter_fields=["user_id", "avatar", "real_name", "nickname"]
        )
        with_user_detail_list = with_user_detail_list if with_user_detail_list else []
        with_user_detail_map = {i["user_id"]: i for i in with_user_detail_list}
        # 详细信息拼接
        for j in page_list:
            j["avatar"] = user_detail_map.get(j["user_id"], {}).get("avatar", [])
            j["real_name"] = user_detail_map.get(j["user_id"], {}).get("real_name", "")
            j["nickname"] = user_detail_map.get(j["user_id"], {}).get("nickname", "")

            j["with_avatar"] = with_user_detail_map.get(j["user_id"], {}).get("avatar", [])
            j["with_real_name"] = with_user_detail_map.get(j["user_id"], {}).get("real_name", "")
            j["with_nickname"] = with_user_detail_map.get(j["user_id"], {}).get("nickname", "")

            # 判断用户分销等级
            if select_level == "first":
                j["level"] = 1
            elif select_level == "second":
                j["level"] = 2
            elif select_level == "third":
                j["level"] = 3
            else:
                if j["user_id"] in first_users:
                    j["level"] = 1
                elif j["user_id"] in second_users:
                    j["level"] = 2
                else:
                    j["level"] = 3
        # ------------------------- section 获取用戶信息 end   ------------------------------------

        # ------------------------- section 項目業務代码 start ------------------------------------
        # 到這裏屬於業務定制代碼，其他項目根據需求修改即可。根據業務進行耦合
        # 查询分销金额
        data_map = db.table("enroll_enroll"). \
            select_raw("""
                enroll_enroll.user_id,
                ROUND(sum(amount),2) as amount_total,
                count(enroll_enroll.id) as count_total
            """). \
            left_join('user_relate_to_user', 'enroll_enroll.user_id', '=', 'user_relate_to_user.user_id'). \
            where_in("enroll_enroll.user_id", [i["user_id"] for i in page_list]). \
            where('user_relate_to_user.user_relate_type_id', '=', 1). \
            where_in('enroll_enroll.enroll_status_code', [80, 668]). \
            where_raw("enroll_enroll.create_time >= user_relate_to_user.created_time"). \
            group_by("enroll_enroll.user_id").get()
        data_map = {i["user_id"]: i for i in data_map}

        #  判断该用户是否是业务人员
        #  如果是业务人员，按照业务人员的分销方案，如果是普通用户则，按照普通用户的营销方案
        role_info, err = RoleService.get_role_list(params={"user_id": with_user_id}, only_first=True)
        is_salesperson = 0
        if role_info and role_info.get("role_key") == "BID-SALESMAN":
            is_salesperson = 1

        def calculate_proportion(amount, select_level, subordinate_user_id):
            amount = str(amount)
            if is_salesperson:  # 是业务员的情况，反三级
                if select_level == 'first':
                    amount = Decimal(amount) * Decimal('0.06')
                elif select_level == 'second':
                    amount = Decimal(amount) * Decimal('0.04')
                elif select_level == 'third':
                    amount = Decimal(amount) * Decimal('0.02')
                else:
                    # 查询全都情况，根据用户ID集合判断，改用的等级
                    if subordinate_user_id in first_users:
                        amount = Decimal(amount) * Decimal('0.06')
                    elif subordinate_user_id in second_users:
                        amount = Decimal(amount) * Decimal('0.04')
                    else:
                        amount = Decimal(amount) * Decimal('0.02')
            else:
                # 不是业务仅仅反一级佣金
                if select_level == "first" or (select_level == "all" and subordinate_user_id in first_users):
                    amount = Decimal(amount) * Decimal('0.04')
                else:
                    amount = 0
            return amount

        for j in page_list:
            j["original_amount"] = float(data_map.get(j["user_id"], {}).get("amount_total", 0))
            j["amount"] = calculate_proportion(
                amount=float(data_map.get(j["user_id"], {}).get("amount_total", 0)),
                select_level=select_level,
                subordinate_user_id=j["user_id"]
            )
            j["order_total"] = float(data_map.get(j["user_id"], {}).get("count_total", 0))
        # ------------------------- section 項目業務代码 end   ------------------------------------

        return {"page": page, "size": size, "total": total, "list": page_list}, None

    # ------------------------------- section 項目業務定制服務 -------------------------------------------
    @staticmethod
    def bind_bxtx_relate(params: dict = None, user_info: dict = None, **kwargs):
        """
        镖行天下绑定用户关系服务
        @note  绑定用户关系 邀请关系和收益关系
        :param params: 请求参数
        :param user_info: 用户信息
        :return: None,err_msg
        """
        user_info, is_pass = force_transform_type(variable=user_info, var_type="dict", default={})
        kwargs, is_pass = force_transform_type(variable=kwargs, var_type="dict", default={})
        params, is_pass = force_transform_type(variable=params, var_type="dict", default={})
        params.update(user_info)
        params.update(kwargs)
        # 获取绑定用户关系

        # 当前用户ID
        user_id, is_pass = force_transform_type(
            variable=params.get('user_id', params.get('id')),
            var_type="int",
            default=0
        )

        # 邀请人ID
        inviter_id, is_pass = force_transform_type(
            variable=params.get('inviter_id'),
            var_type="int",
            default=0
        )

        # 关系与被关系不能是一个人
        if user_id == inviter_id:
            return None, None

        try:
            # 判断是否是一个有效的用户ID
            inviter = BaseInfo.objects.filter(id=inviter_id).first()
            if not inviter:
                return None, None

            # 绑定邀请人
            data, err = UserRelateToUserService.add({
                "user_id": user_id,
                "with_user_id": inviter_id,
                "user_relate_type_value": "invite"
            })
            if err:
                return None, None

            # 邀请人不存在受益人，如果邀请人是业务，则绑定的受益人也是该邀请人
            res, err = RoleService.is_this_role(user_id=inviter_id, role_key="BID-SALESMAN")  # 如果是业务人员
            if res:
                data, err = UserRelateToUserService.add({
                    "user_id": user_id,
                    "with_user_id": inviter_id,
                    "user_relate_type_value": "beneficiary"
                })
                return None, err

            # 查询邀请人的受益人是谁，如果存在则绑定。
            saler = UserRelateToUser.objects.annotate(relate_key=F("user_relate_type__relate_key")).filter(
                user_id=inviter_id, relate_key="beneficiary"
            ).values().first()
            if saler:
                data, err = UserRelateToUserService.add({
                    "user_id": user_id,
                    "with_user_id": saler.get("with_user_id"),
                    "user_relate_type_value": "beneficiary"
                })
                return None, None

        except Exception as e:
            return None, str(e)
        return None, None

    @staticmethod
    def laowu_bind_bxtx_relate(params: dict = None, user_info: dict = None, is_reset=True, **kwargs):
        """
        （劳务通）绑定用户关系服务
        @note  绑定用户关系 邀请关系和收益关系
        :param params: 请求参数
        :param user_info: 用户信息
        :return: None,err_msg
        """
        user_info, is_pass = force_transform_type(variable=user_info, var_type="dict", default={})
        kwargs, is_pass = force_transform_type(variable=kwargs, var_type="dict", default={})
        params, is_pass = force_transform_type(variable=params, var_type="dict", default={})
        params.update(user_info)
        params.update(kwargs)
        # 获取绑定用户关系
        user_id_str, is_pass = force_transform_type(variable=params.get('user_id_list'))  # 当前用户ID
        with_user_id, is_pass = force_transform_type(variable=params.get('with_user_id'))  # 邀请人ID
        relate_key, err = force_transform_type(variable=params.get("relate_key"))
        if relate_key:
            user_relate_type = UserRelateType.objects.filter(relate_key=relate_key).values().first()
        else:
            user_relate_type = UserRelateType.objects.filter(id=params.get("user_relate_type_id")).values().first()
        if not user_relate_type:
            return None, "不是有效的关系类型"
        try:
            # 重置原有关系
            if is_reset:
                UserRelateToUser.objects.filter(with_user_id=with_user_id,
                                                user_relate_type_id=user_relate_type.get("id")).delete()
            # 判断是否是一个有效的用户ID
            user_id_list = parse_integers(user_id_str)
            for i in user_id_list:
                # 绑定邀请人
                data, err = UserRelateToUserService.add({
                    "user_id": i,
                    "with_user_id": with_user_id,
                    "user_relate_type_value": relate_key
                })
                if err:
                    return None, str(err)

        except Exception as e:
            return None, str(e)
        return None, None

    @staticmethod
    def bxtx_relate_user(*args, params: dict = None, **kwargs):
        """
        查询用户关系映射
        :param params: 参数
        """
        # ------------------------- section 参数处理 start ------------------------------------
        kwargs, err = force_transform_type(variable=kwargs, var_type="only_dict", default={})
        params, err = force_transform_type(variable=params, var_type="only_dict", default={})
        params.update(kwargs)

        direct_invite, err = force_transform_type(variable=params.get("direct_invite"), var_type="bool", default=True)
        select_all, err = force_transform_type(variable=params.get("select_all"), var_type="bool", default=False)
        relate_key, err = force_transform_type(variable=params.get("relate_key"))
        if not relate_key:
            relate_key = "invite" if direct_invite else "beneficiary"
            relate_key = "beneficiary" if select_all else relate_key
        user_id, err = force_transform_type(variable=params.get("user_id"), var_type="int")
        if not user_id:
            return None, "不是一个有效的 user_id"
        relate_key, err = force_transform_type(variable=relate_key, var_type="str", default="invite")
        size, err = force_transform_type(variable=params.pop('size', 10), var_type="int", default=10)
        page, err = force_transform_type(variable=params.pop('page', 1), var_type="int", default=1)
        # ------------------------- section 参数处理 end   ------------------------------------

        # ------------------------- section 构建ORM start ------------------------------------
        relate_user_obj = UserRelateToUser.objects.extra(
            select={"created_time": 'DATE_FORMAT(created_time, "%%Y-%%m-%%d %%H:%%i:%%s")'}
        ).annotate(
            relate_key=F("user_relate_type__relate_key"),
            relate_type_name=F("user_relate_type__relate_name"),
            user_name=F("user__user_name"),
            user_phone=F("user__phone"),
            full_name=F("user__full_name"),
            nickname=F("user__nickname"),
            with_user_name=F("with_user__user_name"),
            with_user_phone=F("with_user__phone"),
            with_full_name=F("with_user__full_name"),
            with_nickname=F("with_user__nickname")
        ).filter(with_user_id=user_id)

        # if not select_all:
        relate_user_obj = relate_user_obj.filter(user_relate_type__relate_key=relate_key)

        # 如果是查询间接邀请，则获取出直接邀请的用户
        if not direct_invite and not select_all:
            direct_inviter_users = list(UserRelateToUser.objects.filter(
                with_user_id=user_id, user_relate_type__relate_key="invite"
            ).values("user_id").distinct().order_by("user_id"))

            direct_inviter_users = [i["user_id"] for i in direct_inviter_users]
            relate_user_obj = relate_user_obj.exclude(user_id__in=direct_inviter_users)

        total = relate_user_obj.count()
        relate_user_list = list(relate_user_obj.values(
            "relate_key",
            "relate_type_name",
            "user_name",
            "user_phone",
            "full_name",
            "nickname",
            "with_user_name",
            "with_user_phone",
            "with_full_name",
            "with_nickname",
            "user_id",
            "with_user_id"
        ))
        # ------------------------- section 构建ORM end ------------------------------------

        # ------------------------- section 分页查询 start ------------------------------------
        try:
            page_list = Paginator(relate_user_list, size).page(page)
            page_list = page_list.object_list
        except EmptyPage as e:
            return {"page": page, "size": size, "total": total, "list": []}, None
        # ------------------------- section 分页查询 end   ------------------------------------
        data_map = {}
        EnrollStatisticsServices, err = dynamic_load_class(import_path="xj_enroll.service.enroll_statistics_services",
                                                           class_name="EnrollStatisticsServices")
        if not err:
            data, err = EnrollStatisticsServices.every_one_total(
                params={"user_id_list": [i["user_id"] for i in page_list]}, need_Pagination=False)
            data_map = {i["user_id"]: i for i in data}

        user_detail_list, err = DetailInfoService.get_list_detail(user_id_list=[i["user_id"] for i in page_list],
                                                                  filter_fields=["user_id", "avatar", "real_name"])
        user_detail_list = user_detail_list if user_detail_list else []
        user_detail_map = {i["user_id"]: i for i in user_detail_list}
        for j in page_list:
            j["amount"] = float(data_map.get(j["user_id"], {}).get("amount_total", 0))
            j["order_total"] = float(data_map.get(j["user_id"], {}).get("count_total", 0))
            j["avatar"] = user_detail_map.get(j["user_id"], {}).get("avatar", [])
            j["real_name"] = user_detail_map.get(j["user_id"], {}).get("real_name", "")

        return {"page": page, "size": size, "total": total, "list": page_list}, None

    # ------------------------------- section 項目業務定制服務 -------------------------------------------

    @staticmethod
    def relate_user_tree(*args, params: dict = None, **kwargs):
        """
        用户关系树状
        劳务系统用 最多两级
        :param params: 参数
        """
        # ------------------------- section 参数处理 start ------------------------------------
        kwargs, err = force_transform_type(variable=kwargs, var_type="only_dict", default={})
        params, err = force_transform_type(variable=params, var_type="only_dict", default={})
        params.update(kwargs)
        print(params)
        user_id, err = force_transform_type(variable=params.get("user_id"), var_type="int")
        with_user_id, err = force_transform_type(variable=params.get("with_user_id"), var_type="int")
        user_type, err = force_transform_type(variable=params.get("user_type"), var_type="str")
        relate_key, err = force_transform_type(variable=params.get("relate_key"), var_type="str", default="invite")
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=[
                "relate_key", "relate_type_name", "user_name", "user_phone", "full_name", "nickname",
                "with_user_name", "with_user_phone", "with_full_name", "with_nickname", "user_id_list"
            ],
            alias_dict={"user_id_list": "user_id__in"}
        )
        if user_type == "COMPANY":
            user = BaseInfo.objects.filter(user_type="COMPANY")
            user = user.filter(id=user_id)
            user = user.values("id", "user_name", "full_name", "nickname")
            if user:
                for i in user:
                    relate_user_obj = UserRelateToUser.objects.extra(
                        select={"created_time": 'DATE_FORMAT(created_time, "%%Y-%%m-%%d %%H:%%i:%%s")'}
                    ).annotate(
                        relate_key=F("user_relate_type__relate_key"),
                        relate_type_name=F("user_relate_type__relate_name"),
                        user_name=F("user__user_name"),
                        user_phone=F("user__phone"),
                        full_name=F("user__full_name"),
                        nickname=F("user__nickname"),
                        with_user_name=F("with_user__user_name"),
                        with_user_phone=F("with_user__phone"),
                        with_full_name=F("with_user__full_name"),
                        with_nickname=F("with_user__nickname")
                    ).filter(with_user_id=i['id'], user_relate_type__relate_key=relate_key).values("user_id",
                                                                                                   "user_name",
                                                                                                   "nickname")
                    i['child'] = list(relate_user_obj)
        else:
            user_relate, err = UserRelateToUserService.bxtx_relate_user(
                params={"user_id": user_id, "relate_key": 'enter'})
            if err:
                return None, err
            user = user_relate['list']

        return list(user), None

    @staticmethod
    def group_tree_user(*args, params: dict = None, **kwargs):
        """
          用户关系树状
          劳务系统用 无限极
          :param params: 参数
        """
        with_user_id, err = force_transform_type(variable=params.get("user_id"), var_type="int")
        relate_key, err = force_transform_type(variable=params.get("relate_key"), var_type="str", default="invite")
        exclude_yourself, err = force_transform_type(variable=params.get("exclude_yourself"), var_type="str",
                                                     default="")
        relate_type = db.table("user_relate_type").where('relate_key', relate_key).first()
        if not relate_type:
            return None, '关系不存在'
        sql = generate_query_string(
            "WITH RECURSIVE cte( user_id, with_user_id, user_relate_type_id, LEVEL, is_parent) AS ( SELECT user_relate_to_user.user_id, user_relate_to_user.with_user_id, user_relate_to_user.user_relate_type_id, 0, 1 FROM user_relate_to_user JOIN user_base_info ON user_relate_to_user.with_user_id = user_base_info.id WHERE user_relate_to_user.with_user_id = ? AND user_relate_to_user.user_relate_type_id = ? UNION ALL SELECT child.user_id, child.with_user_id, child.user_relate_type_id, parent.LEVEL + 1, 0 FROM user_relate_to_user AS child JOIN cte AS parent ON child.with_user_id = parent.user_id JOIN user_base_info ON child.user_id = user_base_info.id WHERE child.user_relate_type_id = ? ) SELECT cte.user_id, cte.with_user_id, cte.LEVEL, cte.user_relate_type_id, parent_user.user_name AS parent_user_name, child_user.user_name AS child_user_name, parent_user.nickname AS parent_nickname, child_user.nickname AS child_nickname FROM cte LEFT JOIN user_base_info AS parent_user ON cte.with_user_id = parent_user.id LEFT JOIN user_base_info AS child_user ON cte.user_id = child_user.id ORDER BY LEVEL",
            [with_user_id, relate_type.id, relate_type.id])
        results = db.select(sql)
        if results:
            def convert_to_tree(data, parent_key, child_key):
                tree = []
                lookup = {}

                for item in data:
                    item_id = item[parent_key]
                    if item_id not in lookup:
                        node = {
                            'id': item_id,
                            'user_name': item.get('parent_user_name') if item_id == with_user_id else item.get(
                                'child_user_name'),
                            'nickname': item.get('parent_nickname') if item_id == with_user_id else item.get(
                                'child_nickname'),
                            'child': []
                        }
                        lookup[item_id] = node
                        tree.append(node)

                    child_id = item[child_key]
                    if child_id not in lookup:
                        child_node = {
                            'user_id': child_id,
                            'user_name': item.get('child_user_name'),
                            'nickname': item.get('child_nickname'),
                            'child': []
                        }
                        lookup[child_id] = child_node
                        lookup[item_id]['child'].append(child_node)

                return tree

            results_list = convert_to_tree(results, 'with_user_id', 'user_id')
        else:
            results = db.table("user_base_info").select("id as user_id", "nickname", "user_name").where('id',
                                                                                                        with_user_id).get()
            results_list = results.items
            for item in results_list:
                item['child'] = []

        if exclude_yourself:
            return [child for child in results_list[0]["child"]], None

        return results_list[0], None
