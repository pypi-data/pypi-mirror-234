# encoding: utf-8
"""
@project: djangoModel->user_info_service
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 用户信息服务
@created_time: 2022/6/27 19:51
"""
from django.core.paginator import Paginator, EmptyPage
from django.db.models import F, Case, When, Value, CharField, OuterRef, Subquery
from django.db.models.functions import Coalesce
from orator import DatabaseManager

from config.config import JConfig
from ..models import ExtendField, DetailInfo, BaseInfo, UserSubCompany, UserApplyRecord
from ..utils.custom_tool import *

# orator ORM 初始化
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


class DetailInfoService:
    # 用户基础表字段列表
    user_base_fields = [i.name for i in BaseInfo._meta.fields]
    # 用户详情表字段
    user_detail_fields = [i.name for i in DetailInfo._meta.fields] + ["user_id"]
    user_detail_expect_extend = [i.name for i in DetailInfo._meta.fields if not "field_" in i.name] + ["user_id"]
    user_detail_remove_fields = [i.name for i in DetailInfo._meta.fields if "field_" in i.name] + ["id", "user"]
    # 详情信息扩展字段获取。该行代码在执行manage.py makemigragtion 会报表不存在 20230822 by Sieyoo
    # field_map_list = list(ExtendField.objects.all().values("field", 'field_index'))
    field_map_list = list(ExtendField.objects.all().values("field", 'field_index')) if ExtendField.objects.all().values(
        "field", 'field_index') else list()

    @staticmethod
    def get_list_detail(params: dict = None, user_id_list: list = None, filter_fields: list = None, **kwargs):
        """
        详细信息列表
        :param filter_fields: 需要过滤的字段
        :param params: 搜索参数
        :param user_id_list: 用户ID列表。请注意：如果传递过来的参数不是有效的列表，则按照正常的分页搜索返回。
        :return: list,err
        """
        params, is_pass = force_transform_type(variable=params, var_type="dict", default={})
        page, is_pass = force_transform_type(variable=params.pop('page', 1), var_type="int", default=1)
        size, is_pass = force_transform_type(variable=params.pop('size', 10), var_type="int", default=10)
        user_group_id, is_pass = force_transform_type(variable=params.get('user_group_id'), var_type="int")
        user_role_id, is_pass = force_transform_type(variable=params.get('user_role_id'), var_type="int")

        # 查询排序字段处理
        sort = params.pop('sort', "-register_time")
        sort = sort if sort in ["register_time", "-register_time", "user_id", "-user_id"] else "-id"

        # 扩展字段映射字典
        field_map_list = DetailInfoService.field_map_list
        field_map = {item['field_index']: item['field'] for item in field_map_list}
        reversal_filed_map = {item['field']: item['field_index'] for item in field_map_list}

        # 默认返回字段去掉与的敏感信息
        default_field_list = DetailInfoService.user_detail_expect_extend + list(field_map.values()) + [
            "is_delete", "user_name", "full_name", "nickname", "user_id", "phone",
            "is_using", "user_identity", "subcompany_name"
        ]
        all_field_list = DetailInfoService.user_detail_expect_extend + DetailInfoService.user_base_fields + list(
            field_map.values()) + ["subcompany_name"]
        # 过滤字段处理
        filter_fields = format_list_handle(
            param_list=filter_fields_handler(
                input_field_expression=filter_fields,
                default_field_list=default_field_list,
            ),
            filter_filed_list=all_field_list,
            alias_dict=reversal_filed_map
        )
        # 查询ORM构建
        subcompany_name_subquery = UserSubCompany.objects.filter(id=OuterRef('subcompany_id')).values('name')
        detail_info_obj = DetailInfo.objects.extra(
            select={"register_time": 'DATE_FORMAT(user_base_info.register_time, "%%Y-%%m-%%d %%H:%%i:%%s")'}
        ).filter(user__is_delete=0).annotate(
            user_name=F("user__user_name"),
            full_name=F("user__full_name"),
            nickname=F("user__nickname"),
            phone=F("user__phone"),
            email=F("user__email"),
            user_info=F("user__user_info"),
            privacies=F("user__privacies"),
            user_type=F("user__user_type"),
            is_delete=F("user__is_delete"),
            is_using=F("user__is_using"),
            user_identity=F("user__user_identity"),
            subcompany_name=Subquery(subcompany_name_subquery),
        ).order_by(sort).values(*filter_fields)
        total = 0

        # id搜索,并且不分页，作为服务提供者
        # 搜索字典过滤处理,过滤掉不允许搜索的字段
        if not user_id_list is None and isinstance(user_id_list, list):
            # id列表参数校验，确保每一个参数都是有效得到int类型
            validate_user_id_list = []
            for i in user_id_list:
                var, valid = force_transform_type(variable=i, var_type="int")
                if valid:
                    continue
                validate_user_id_list.append(var)
            validate_user_id_list = list(set(validate_user_id_list))

            # 进行参数搜索
            res_list = detail_info_obj.filter(user_id__in=validate_user_id_list)

        elif user_role_id:
            res_obj = db.table("role_user_to_role"). \
                select("role_user_to_role.role_id",
                       "role_user_to_role.user_id",
                       "uuid",
                       "user_name",
                       "full_name",
                       "nickname",
                       "phone",
                       "email",
                       "user_info",
                       "user_type",
                       "privacies",
                       "register_time",
                       "is_delete",
                       "real_name",
                       "sex",
                       "birth",
                       "tags",
                       "signature",
                       "avatar",
                       "cover",
                       "language",
                       "region_code",
                       "more",
                       "field_1",
                       "field_2",
                       "field_3",
                       "field_4",
                       "field_5",
                       "field_6",
                       "field_7",
                       "field_8",
                       "field_9",
                       "field_10",
                       "field_11",
                       "field_12",
                       "field_13",
                       "field_14",
                       "field_15",
                       ). \
                left_join("user_detail_info", "user_detail_info.user_id", "=", "role_user_to_role.user_id"). \
                left_join("user_base_info", "user_base_info.id", "=", "role_user_to_role.user_id"). \
                where("role_user_to_role.role_id", user_role_id)

            result_list = res_obj.paginate(size, page)
            total = result_list.total
            res_data = filter_result_field(
                result_list=filter_result_field(  # 扩展字段替换
                    result_list=result_list,
                    alias_dict=field_map,
                ),
                remove_filed_list=DetailInfoService.user_detail_remove_fields,  # 移除未配置的扩展字段已经主键ID
                alias_dict={"user": "user_id", "cover": "user_cover", "region_code": "user_region_code"}
                # 外键字段还原成ID，并起别名
            )

            return {'size': int(size), 'page': int(page), 'total': total, 'list': res_data}, None
        elif user_group_id:
            res_obj = db.table("role_user_to_group"). \
                select("role_user_to_group.user_group_id",
                       "role_user_to_group.user_id",
                       "uuid",
                       "user_name",
                       "full_name",
                       "nickname",
                       "phone",
                       "email",
                       "user_info",
                       "user_type",
                       "privacies",
                       "register_time",
                       "is_delete",
                       "real_name",
                       "sex",
                       "birth",
                       "tags",
                       "signature",
                       "avatar",
                       "cover",
                       "language",
                       "region_code",
                       "more",
                       "field_1",
                       "field_2",
                       "field_3",
                       "field_4",
                       "field_5",
                       "field_6",
                       "field_7",
                       "field_8",
                       "field_9",
                       "field_10",
                       "field_11",
                       "field_12",
                       "field_13",
                       "field_14",
                       "field_15",
                       ). \
                left_join("user_detail_info", "user_detail_info.user_id", "=", "role_user_to_group.user_id"). \
                left_join("user_base_info", "user_base_info.id", "=", "role_user_to_group.user_id"). \
                where("role_user_to_group.user_group_id", user_group_id)

            result_list = res_obj.paginate(size, page)
            total = result_list.total
            res_data = filter_result_field(
                result_list=filter_result_field(  # 扩展字段替换
                    result_list=result_list,
                    alias_dict=field_map,
                ),
                remove_filed_list=DetailInfoService.user_detail_remove_fields,  # 移除未配置的扩展字段已经主键ID
                alias_dict={"user": "user_id", "cover": "user_cover", "region_code": "user_region_code"}
                # 外键字段还原成ID，并起别名
            )

            return {'size': int(size), 'page': int(page), 'total': total, 'list': res_data}, None
        else:
            search_params = format_params_handle(
                param_dict=params,
                filter_filed_list=all_field_list + ["register_time_start", "register_time_end", "user_id_list"],
                alias_dict=reversal_filed_map
            )
            search_params = format_params_handle(
                param_dict=search_params,
                alias_dict={
                    "user_type": "user_type__contains",
                    "user_name": "user_name__contains",
                    "nickname": "nickname__contains",
                    "email": "email__contains",
                    "phone": "phone__contains",
                    "full_name": "full_name__contains",
                    "real_name": "real_name__contains",
                    "register_time_start": "user__register_time__gte",
                    "register_time_end": "user__register_time__lte",
                    "user_id_list": "user__id__in"
                }
            )
            list_set = detail_info_obj.filter(**search_params)
            total = list_set.count()
            paginator = Paginator(list_set, size)
            try:
                list_set = paginator.page(page)
            except EmptyPage:
                list_set = paginator.page(paginator.num_pages)
            except Exception as e:
                return None, e.__str__()
            res_list = list(list_set.object_list)

        res_data = filter_result_field(
            result_list=filter_result_field(  # 扩展字段替换
                result_list=res_list,
                alias_dict=field_map,
            ),
            remove_filed_list=DetailInfoService.user_detail_remove_fields,  # 移除未配置的扩展字段已经主键ID
            alias_dict={"user": "user_id", "cover": "user_cover", "region_code": "user_region_code"}  # 外键字段还原成ID，并起别名
        )
        # ======================= section 追加角色和权限信息 由于前后台用户暂时公用一个接口 增加限制 start ==============================
        if params.get("need_role_data"):
            for res in res_data:
                # ================== section 获取角色模块信息 start ============================
                # 获取用户的部门信息
                try:
                    RoleService, import_err = dynamic_load_class(import_path="xj_role.services.role_service",
                                                                 class_name="RoleService")
                    if import_err:
                        raise Exception(import_err)
                    user_role_list, err = RoleService.get_user_role_info(user_id=res["user_id"],
                                                                         field_list=["role_id", "role_name"])
                    user_role_name_list = [i["role_name"] for i in user_role_list]
                    user_role_list = [i["role_id"] for i in user_role_list]

                except Exception:
                    user_role_list = []
                    user_role_name_list = []
                # 获取角色的信息信息
                try:
                    UserGroupService, import_err = dynamic_load_class(import_path="xj_role.services.user_group_service",
                                                                      class_name="UserGroupService")
                    if import_err:
                        raise Exception(import_err)
                    user_group_list, err = UserGroupService.get_user_group_info(user_id=res["user_id"],
                                                                                field_list=["user_group_id",
                                                                                            "group_name"])
                    user_group_name_list = [i["group_name"] for i in user_group_list]
                    user_group_list = [i["user_group_id"] for i in user_group_list]
                except Exception:
                    user_group_list = []
                    user_group_name_list = []
                res["user_role_list"] = user_role_list
                res["user_group_list"] = user_group_list
                res["user_role_name_list"] = user_role_name_list
                res["user_group_name_list"] = user_group_name_list
        # ======================= section 追加角色和权限信息 由于前后台用户暂时公用一个接口 增加限制 end ==============================

        # 分情况返回数据
        if not user_id_list is None and isinstance(user_id_list, list):
            return res_data, None
        else:
            return {'size': int(size), 'page': int(page), 'total': total, 'list': res_data}, None

    @staticmethod
    def get_detail(user_id: int = None, search_params: dict = None, filter_fields: "str|list" = None, **kwargs):
        """
        获取当前用户的基础信息和详细信息集合
        :param search_params: 根据参数搜索，note 支持用户唯一值搜索。如果多条取第一条。
        :param user_id: 通过用户ID搜索
        :param filter_fields: 过滤字段
        :return: detail_info,err_msg
        """
        # ==================== section 参数验证 start ==========================
        search_params, is_pass = force_transform_type(variable=search_params, var_type="dict", default={})
        user_id, is_pass = force_transform_type(variable=user_id, var_type="int")
        search_params = format_params_handle(
            param_dict=search_params,
            filter_filed_list=["user_name", "full_name", "nickname", "phone", "email"]
        )
        if not user_id and not search_params:
            return None, "参数错误，无法检索用户"
        # ==================== section 参数验证 end    ==========================

        # ======================= section 判断是否是一个合法用户 start ==============================
        user_base = BaseInfo.objects.extra(
            select={'register_time': 'DATE_FORMAT(register_time, "%%Y-%%m-%%d %%H:%%i:%%s")'})
        # 允许使用用户ID或者使用条件参数搜素
        if user_id:
            user_base = user_base.filter(id=user_id).first()
        else:
            user_base = user_base.filter(**search_params).first()
        if not user_base:
            return None, '用户不存在'
        user_id = user_base.id
        # ======================= section 判断是否是一个合法用户 end   ==============================

        # ======================= section 不存在详细信息,则创建 start   ==============================
        is_has_detail = DetailInfo.objects.filter(user_id=user_id).first()
        if not is_has_detail:
            data, err = DetailInfoService.create_or_update_detail({"user_id": user_id})
            if err:
                return None, err

        # ======================= section 不存在详细信息,则创建 end   ==============================

        # ======================= section ORM查村字段过滤 start ==============================
        # note 这里出于性能考虑，在ORM执行select的时候减少查询的字段
        index_to_field_map = {item['field_index']: item['field'] for item in DetailInfoService.field_map_list}
        field_to_index_map = {item['field']: item['field_index'] for item in DetailInfoService.field_map_list}
        all_field_list = DetailInfoService.user_detail_expect_extend + list(
            index_to_field_map.values()) + DetailInfoService.user_base_fields  # 得到所有需要过滤的字段
        # 前端输入的过滤字段，替换成可搜索的数据库字段
        orm_filter_fields = format_list_handle(
            param_list=filter_fields_handler(
                input_field_expression=filter_fields,
                all_field_list=all_field_list
            ),
            alias_dict=field_to_index_map
        )
        # 用户基础信息使用使用select_related外键查询搜索，所以需要加上user前缀
        orm_filter_fields = format_list_handle(
            param_list=orm_filter_fields,
            alias_dict={i: "user__" + i for i in DetailInfoService.user_base_fields}  # 用户的基础信息添加前缀
        )
        # ======================= section ORM查村字段过滤 end   ==============================

        # note 使用select_related("user")是为了适配数据库结构变动，而不需要在修改代码。
        user_detail = DetailInfo.objects.select_related("user").extra(select={
            'birth': 'DATE_FORMAT(birth, "%%Y-%%m-%%d %%H:%%i:%%s")',
            "user__register_time": 'DATE_FORMAT(register_time, "%%Y-%%m-%%d %%H:%%i:%%s")',
        }).filter(user_id=user_id).values(*orm_filter_fields).first()

        # ================== section 获取角色模块信息 start ============================
        # 获取用户的部门信息
        try:
            RoleService, import_err = dynamic_load_class(import_path="xj_role.services.role_service",
                                                         class_name="RoleService")
            if import_err:
                raise Exception(import_err)
            user_role_list, err = RoleService.get_user_role_info(user_id=user_id, field_list=["role_id", "role_name"])
            user_role_name_list = [i["role_name"] for i in user_role_list]
            user_role_list = [i["role_id"] for i in user_role_list]

        except Exception:
            user_role_list = []
            user_role_name_list = []
        # 获取角色的信息信息
        try:
            UserGroupService, import_err = dynamic_load_class(import_path="xj_role.services.user_group_service",
                                                              class_name="UserGroupService")
            if import_err:
                raise Exception(import_err)
            user_group_list, err = UserGroupService.get_user_group_info(user_id=user_id,
                                                                        field_list=["user_group_id", "group_name"])
            user_group_name_list = [i["group_name"] for i in user_group_list]
            user_group_list = [i["user_group_id"] for i in user_group_list]
        except Exception:
            user_group_list = []
            user_group_name_list = []
        user_detail["user_role_list"] = user_role_list
        user_detail["user_group_list"] = user_group_list
        user_detail["user_role_name_list"] = user_role_name_list
        user_detail["user_group_name_list"] = user_group_name_list
        # ================== section 获取角色模块信息 end    ============================

        # 获取用户分子公司信息
        try:
            subcompany = UserSubCompany.objects.filter(id=user_detail["subcompany"]).first()
            if subcompany:
                user_detail["subcompany_name"] = subcompany.name
        except:
            pass

        # =========== section 字段替换 start =====================
        # note 第二次过滤，为了过滤功能的完整性。在这支持滤掉自定义拼接的字段。
        # 字段恢复成配置的扩展字段，替换掉用户基础信息的外键前缀
        filter_dict = format_params_handle(
            param_dict=format_params_handle(
                param_dict=user_detail,
                alias_dict=index_to_field_map,
                is_remove_null=False
            ),
            alias_dict={"user__" + i: i for i in DetailInfoService.user_base_fields},  # 去除用户的基础信息的字段前缀
            is_remove_null=False
        )
        # 移除未配置的扩展字段
        split_joint = ["user_role_list", "user_group_list", "user_role_name_list", "user_group_name_list",
                       "subcompany_name"]  # 拼接字段白名单
        filter_dict = format_params_handle(
            param_dict=filter_dict,
            filter_filed_list=filter_fields_handler(
                input_field_expression=filter_fields,
                all_field_list=all_field_list + split_joint
            ),
            alias_dict={"cover": "user_cover", "user": "user_id", "region_code": "user_region_code"},
            remove_filed_list=["id"],
            is_remove_null=False
        )
        # =========== section 字段替换 end   =====================

        # ================== section 追加信息 start ==============
        # 获取用户审核信息
        try:
            result_dict = ["UN_APPLY", "VERIFY_PASS", "VERIFYING", "VERIFY_REJECT"]
            real_name_result = result_dict[int(filter_dict["real_name_is_pass"])]  # 实名认证状态
            audit_result = result_dict[int(filter_dict["audit_status"])]  # 镖师认证状态
            if real_name_result == "VERIFY_REJECT":  # 审核不通过才需要原因
                reply_record = UserApplyRecord.objects.filter(user_id=user_id, apply_type_id=1, result=real_name_result).order_by("-id").values("reject_reason").first()
                if reply_record:
                    filter_dict["reject_real_name_reason"] = reply_record["reject_reason"]
            elif real_name_result == "VERIFY_PASS":  # 用户审核通过时间
                reply_record = UserApplyRecord.objects.extra(select={
                        "verify_time": 'DATE_FORMAT(verify_time, "%%Y-%%m-%%d %%H:%%i:%%s")',
                    }).filter(user_id=user_id, apply_type_id=1, result=real_name_result).order_by("-id").values("verify_time").first()
                if reply_record:
                    filter_dict["real_name_verify_time"] = reply_record["verify_time"]
            if audit_result == "VERIFY_REJECT":  #
                reply_record = UserApplyRecord.objects.filter(user_id=user_id, apply_type_id=2, result=audit_result).order_by("-id").values("reject_reason").first()
                if reply_record:
                    filter_dict["reject_audit_status_reason"] = reply_record["reject_reason"]
            elif audit_result == "VERIFY_PASS":
                reply_record = UserApplyRecord.objects.extra(select={
                        "verify_time": 'DATE_FORMAT(verify_time, "%%Y-%%m-%%d %%H:%%i:%%s")',
                    }).filter(user_id=user_id, apply_type_id=2, result=audit_result).order_by("-id").values("verify_time").first()
                if reply_record:
                    filter_dict["audit_status_verify_time"] = reply_record["verify_time"]
        except:
            pass

        # ================== section 追加信息 end ================
        return filter_dict, None

    @staticmethod
    def create_or_update_detail(params: dict = None, **kwargs):
        """
        添加或者更新用户的详细信息
        :param params: 添加/修改参数
        :return: None,err_msg
        """
        # 参数判断
        kwargs, is_pass = force_transform_type(variable=kwargs, var_type="dict", default={})
        params, is_pass = force_transform_type(variable=params, var_type="dict", default={})
        params.update(kwargs)

        user_id, is_pass = force_transform_type(variable=params.pop('user_id', None), var_type="int")
        if not user_id:
            return None, "参数错误,user_id不能为空"
        # 判断用户是否存在
        user_base = BaseInfo.objects.filter(id=user_id)
        user_base_info = user_base.first()
        if not user_base_info:
            return None, '用户不存在'
        # =========== section 获取扩展字段的映射，默认值 start =================
        extend_field_list = ExtendField.objects.all().values("field", 'field_index', 'default')
        alias_dict = {item['field']: item['field_index'] for item in extend_field_list}  # 字段还原映射字典
        default_map = {item['field_index']: item['default'] for item in extend_field_list if
                       not item['default'] is None}  # 默认字段
        filter_filed_list = [i.name for i in DetailInfo._meta.fields]  # 字段列表
        # 强制类型转换,防止修改报错
        filter_filed_list.remove("id")
        filter_filed_list.remove("birth")
        filter_filed_list.remove("region_code")
        filter_filed_list.remove("more")
        # filter_filed_list.append("birth|date")
        filter_filed_list.append("region_code|int")
        filter_filed_list.append("more|dict")
        filter_filed_list.append("subcompany_id|int")
        # =========== section 获取扩展字段的映射，默认值 end   =================

        # =========== section 把扩展字段还原成 start =================
        # 剔除掉不是配置的扩展字段,还有原表的字段
        transformed_params = format_params_handle(
            param_dict=format_params_handle(
                param_dict=params,
                alias_dict=alias_dict
            ),
            filter_filed_list=filter_filed_list,
        )
        transformed_params.setdefault("user_id", user_id)
        # print("transformed_params >>>", transformed_params)
        # =========== section 把扩展字段还原成 end   =================
        # =========== section 进行数据库操作 start ============
        try:
            # 判断是否添加过
            detail_user_obj = DetailInfo.objects.filter(user_id=user_id)
            if not detail_user_obj.first():
                # 没有添加，进行添加操作
                transformed_params.pop("id", None)  # 添加的时候不能有ID主键，防止主键冲突
                # 在添加的时候给字段默认值
                for field_index, default in default_map.items():
                    transformed_params.setdefault(field_index, default)

                DetailInfo.objects.create(**transformed_params)
            else:
                # 添加过进行跟新
                detail_user_obj.update(**transformed_params)
            return None, None
        except Exception as e:
            return None, "参数配置错误：" + str(e)
        # =========== section 进行数据库操作 end   ============

    @staticmethod
    def get_extend_fields():
        """
        获取用户表扩展字段，前端渲染使用
        :return: fields_list,None
        """
        fields = ExtendField.objects.order_by("-sort").all().to_json()
        return fields, None
