# encoding: utf-8
"""
@project: djangoModel->user_apply_services
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 用户审批服务
@created_time: 2023/8/30 17:09
"""
import datetime
from collections import defaultdict

from django.core.paginator import Paginator, EmptyPage
from django.db.models import F, Count

from .user_service import UserService
from ..models import UserApplyType, BaseInfo, UserApplyRecord
from ..services.user_detail_info_service import DetailInfoService
from ..utils.custom_tool import format_params_handle, force_transform_type

"""
设计思路：
所有的审核都有四个状态
{
"field": "real_name_is_pass", 
"status_map": [{"label": "UN_APPLY", "value": "0"}, {"label": "VERIFY_PASS", "value": "1"}, {"label": "VERIFYING", "value": "2"}, {"label": "VERIFY_REJECT", "value": "3"}]
}

执行步骤：
1. 仅仅在 未申请/审核驳回 状态可以添加申请。
2. 通过联动用户状态，用户字段改成通过。
3. 审核不通过，联动用户字段改成不通过。
4. 审核不通过，用户可以继续提交申请，并生成一条新的记录。
5. 审批记录仅仅有三个状态：待审核、通过、审核驳回, 没有提交记录就是未审批。

核心：
整个审批过程中需要保证 用户详情状态与审批记录结果一致。
审核通过的审批，联动了用户详情里面状态，由于 ‘仅仅在 未申请/审核驳回 状态可以添加申请。’ 所以不可以重复申请审批了。达到了状态一致。
用户审批记录与用户主表和用户详细表的审核状态结合。

各端判断：
1. 移动端使用用户详情里面的字段
2. 后台管理端仅仅看审批记录，看已通过的需要在在审批管理里面，选择已通过卡片就可以看到通过审批记录，这些记录代表审核通过的用户。

查询：
审批主表，联表：用户主表、用户详情表。

审批类型：
代表不通的审批类型，且配置了，用户详情表与审批结果的映射。

表结构：
-- 用户状态审批表
CREATE TABLE `user_apply_record` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `user_id` int NOT NULL COMMENT '申请的用户ID',
  `apply_type_id` int NOT NULL COMMENT '审批类型',
  `verify_user_id` int NOT NULL COMMENT '审核人',
  `result` varchar(500) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT 'VERIFYING' COMMENT '审核结果: 通过：PASS；拒绝：REJECT；忽略：IGNORE; 审核中：VERIFYING',
  `remark` varchar(500) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT '' COMMENT '备注',
  `reject_reason` varchar(500) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT '' COMMENT '拒绝理由',
  `snapshot` json DEFAULT NULL COMMENT '用户状态快照',
  `verifyed_time` timestamp NULL DEFAULT NULL COMMENT '审核时间',
  `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8_unicode_ci COMMENT='用户状态审批表';
-- 用户申请类型
CREATE TABLE `user_apply_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `value` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '类型搜索key',
  `type_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '类型名称',
  `description` varchar(500) NOT NULL COMMENT '描述',
  `config` json DEFAULT NULL COMMENT '配置，联动字段配置',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='用户申请类型';
"""


class UserApplyServices:
    VERIFYING = "VERIFYING"
    VERIFY_PASS = "VERIFY_PASS"
    VERIFY_REJECT = "VERIFY_REJECT"
    IGNORE = "IGNORE"
    UN_APPLY = None

    # 审核结果中文映射
    result_to_cn = {
        "VERIFYING": "审核中",
        "VERIFY_PASS": "审核通过",
        "VERIFY_REJECT": "审核拒绝"
    }

    # 审批类型配置案例
    apply_type_config_example = {
        "field": "real_name_is_pass",
        "status_map": [  # 规定的映射，后面的数字根据业务而定
            {"label": "UN_APPLY", "value": "0"},
            {"label": "VERIFY_PASS", "value": "1"},
            {"label": "VERIFYING", "value": "2"},
            {"label": "VERIFY_REJECT", "value": "3"}
        ]
    }

    @staticmethod
    def add_apply_record(params: dict = None, **kwargs):
        """
        添加审批记录, 联动用户状态修改成审核中
        :return: None, err
        """
        # 参数融合
        kwargs, err = force_transform_type(variable=kwargs, var_type="dict", default={})
        params, err = force_transform_type(variable=params, var_type="dict", default={})
        params.update(kwargs)

        # --------------------- section 参数有效性验证 start ------------------------
        try:
            # 类型验证
            params = format_params_handle(
                param_dict=params,
                is_remove_empty=False,
                filter_filed_list=[
                    "apply_type_id|int", "user_id|int", "verify_user_id|int", "result|str", "remark|str",
                    "reject_reason|str", "snapshot|dict", "created_time|date", "verify_files|dict"
                ]
            )
            # 必填验证
            for i in ["apply_type_id", "user_id"]:
                if not params.get(i):
                    raise ValueError("不是一个有效的 " + i)
            # 默认初审 审核中
            params.setdefault("result", UserApplyServices.VERIFYING)
        except ValueError as e:
            return None, str(e)

        # 获取申请人基础信息
        user_base_info = BaseInfo.objects.filter(id=params.get("user_id", 0), is_delete=0).values().first()
        if not user_base_info:
            return None, "不存在user_id为 " + str(params.get("params") or " ") + "用户"

        # 获取申请类型
        apply_type_info = UserApplyType.objects.filter(id=params.get("apply_type_id")).values().first()
        if not apply_type_info:
            return None, "不是一个有效的审批类型"
        # --------------------- section 参数有效性验证 end  ------------------------

        # --------------------- section 审批配置校验 start ----------------------------
        # 审批配置信息
        apply_type_config = apply_type_info.get("config", {})
        status_map = apply_type_config.get("status_map", {})
        status_field = apply_type_config.get("field")
        status_value_map = {i["label"]: i["value"] for i in status_map if i.get("label") and i.get("value")}
        if not status_field:
            return None, "审批配置错误，无法读取到审批状态字段"
        if not status_value_map.get(UserApplyServices.VERIFYING) or \
                not status_value_map.get(UserApplyServices.VERIFY_PASS) or \
                not status_value_map.get(UserApplyServices.VERIFY_REJECT):
            return None, "审批配置错误，请检查审类型配置"
        # --------------------- section 审批配置校验 end  ----------------------------

        # --------------------- section 用户详情状态核验 start ----------------------------
        # 获取详细信息
        user_detail_info, err = DetailInfoService.get_detail(user_id=params["user_id"])
        if err:
            return None, "获取用户详细信息失败：" + err
        if not user_detail_info:
            return None, "没有user_id为 （" + str(params.get("user_id", "空")) + "） 的用户详细信息"

        # 审批可提交验证
        verify_status = user_detail_info.get(status_field, "null")
        # 如果为空认为我提交过审核，等同于UN_APPLY
        if verify_status == "null":
            return None, "审批配置错误，无法读取到该用户的审批状态，请检查扩展字段配置"
        if verify_status == status_value_map.get(UserApplyServices.VERIFYING):
            return None, "您有正在审核的申请"
        if verify_status == status_value_map.get(UserApplyServices.VERIFY_PASS):
            return None, "您的审批愿意通过，无需再次申请"
        # --------------------- section 用户详情状态核验 end  ----------------------------

        # --------------------- section 审批及联动修改 start ----------------------------
        # 联动修改用户详细信息
        data, err = DetailInfoService.create_or_update_detail(
            params={
                "user_id": params.get("user_id"),
                status_field: status_value_map.get(UserApplyServices.VERIFYING)
            }
        )
        if err:
            return None, "联动用户详情修改异常：" + err

        # 创建申请记录
        try:
            params.setdefault("snapshot", {
                "field": status_field,
                "update_before": verify_status,
                "update_after": status_value_map.get("verifying")
            })
            apply_record = UserApplyRecord(**params)
            apply_record.save()
        except Exception as e:
            return None, str(e)
        # --------------------- section 审批及联动修改 end  ----------------------------

        return None, None

    @staticmethod
    def edit_apply_record(params: dict = None, pk: int = None, **kwargs):
        """
        添加审批记录, 联动用户状态修改成审核中
        :return: None, err
        """
        # ---------------------- section 参数融合,类型校验 start ----------------------
        kwargs, err = force_transform_type(variable=kwargs, var_type="dict", default={})
        params, err = force_transform_type(variable=params, var_type="dict", default={})
        params.update(kwargs)
        pk, err = force_transform_type(variable=pk, var_type="int")
        if pk is None:
            return None, "参数错误，不是一个有效的pk"
        # ---------------------- section 参数融合，类型校验 end  ----------------------

        # --------------------- section 参数有效性验证 start  ------------------------
        # 检查修改的数据是否存在
        instance = UserApplyRecord.objects.filter(id=pk)
        record_instance_info = instance.values(
            "id", "apply_type_id", "user_id", "verify_user_id", "result", "remark",
            "reject_reason", "snapshot", "verify_files", "verify_time", "updated_time",
            "created_time",
        ).first()
        if not record_instance_info:
            return None, "数据不存在，无法修改"

        # 参数白名单，类型验证
        try:
            params = format_params_handle(
                param_dict=params,
                is_remove_empty=False,
                filter_filed_list=[
                    "result|str", "remark|str", "reject_reason|str", "verify_files|dict",
                    "snapshot|dict", "created_time|date", "verify_time|date", "verify_user_id|int"
                ]
            )
            if not params.get("verify_user_id"):
                return None, "审批人不能为空"

        except ValueError as e:
            return None, str(e)
        # --------------------- section 参数有效性验证 end  ------------------------

        # --------------------- section 获取配置，校验参数，校验用户状态 start ------------------------
        # 获取申请类型
        apply_type_info = UserApplyType.objects.filter(id=record_instance_info.get("apply_type_id")).values().first()
        if not apply_type_info:
            return None, "不是一个有效的审批类型"

        # 审批配置信息
        apply_type_config = apply_type_info.get("config", {})
        status_map = apply_type_config.get("status_map", {})
        status_field = apply_type_config.get("field")
        status_value_map = {i["label"]: i["value"] for i in status_map if i.get("label") and i.get("value")}
        if not status_field:
            return None, "审批配置错误，无法读取到审批状态字段"

        # 可审批验证
        user_detail_info, err = DetailInfoService.get_detail(user_id=record_instance_info.get("user_id"))
        if err or not user_detail_info:
            return None, "不存在user_id为 " + str(params.get("params") or "-") + "用户"

        verify_status = user_detail_info.get(status_field, "null")
        if verify_status == "null":
            return None, "审批配置错误，无法读取到该用户的审批状态"

        verify_result = params.get("result")
        if verify_result and not (
                verify_result == UserApplyServices.VERIFY_PASS or verify_result == UserApplyServices.VERIFY_REJECT):
            return None, "不是一个有效的审核类型"

        # --------------------- section 获取配置，校验参数，校验用户状态 end  ------------------------

        # --------------------- section 审批修改,以及联动修改 start ------------------------
        # 联动用户详情状态表修改
        if verify_result:
            user_detail_status = status_value_map.get(verify_result)
            # 联动修改用户详细信息
            user_params = {
                "user_id": record_instance_info.get("user_id"),
                status_field: user_detail_status
            }
            user_params.update(**record_instance_info["verify_files"])
            print("user_params", user_params)
            data, err = DetailInfoService.create_or_update_detail(
                params=user_params
            )
            if err:
                return None, "联动用户详情修改异常：" + err
            params.setdefault("verify_time", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        # 联动用户身份修改
        if record_instance_info.get("apply_type_id") == 2 and params.get("result") == "VERIFY_PASS":  # 镖师审核通过
            data, err = UserService.bind_user_identity(record_instance_info.get("user_id"), 2)
            if err:
                return None, "联动用户身份异常：" + err
        # 编辑可修改参数
        instance.update(**params)
        # --------------------- section 审批修改,以及联动修改 end  ------------------------

        return None, None

    @staticmethod
    def apply_record_list(params: dict = None, **kwargs):
        # 参数融合
        kwargs, err = force_transform_type(variable=kwargs, var_type="dict", default={})
        params, err = force_transform_type(variable=params, var_type="dict", default={})
        params.update(kwargs)

        page, err = force_transform_type(variable=params.get("page"), var_type="int", default=1)
        size, err = force_transform_type(variable=params.get("size"), var_type="int", default=10)
        sort = params.get("sort", "-created_time")
        sort = sort if sort in ["verify_time", "updated_time", "created_time", "-verify_time", "-updated_time",
                                "-created_time"] else "-created_time"
        user_real_name = params.get("user_real_name")
        user_id_card = params.get("user_id_card")

        params = format_params_handle(
            param_dict=params,
            is_remove_empty=False,
            filter_filed_list=[
                "result|str", "remark|str", "reject_reason|str", "verify_files|dict",
                "snapshot|dict", "created_time|date", "verify_time|date", "user_id_list|list_int",
                "verify_user_id_list|list_int", "created_time|date",
                "user_phone", "apply_type_id",
                "created_time_start", "created_time_end", "verify_time_start", "verify_time_end"
            ],
            alias_dict={
                "user_id_list": "user_id__in", "verify_user_id_list": "verify_user_id__in",
                "created_time_start": "created_time__gte",
                "created_time_end": "created_time__lte",
                "verify_time_start": "verify_time__gte",
                "verify_time_end": "verify_time__lte",
            }
        )
        if user_real_name:
            params.update({"verify_files__real_name__icontains": user_real_name})
        if user_id_card:
            params.update({"verify_files__id_card__icontains": user_id_card})
        print("params", params)
        record_obj = UserApplyRecord.objects.annotate(
            apply_type_value=F("apply_type__value"),
            apply_type_name=F("apply_type__type_name"),
            user_user_name=F("user__user_name"),
            user_nickname=F("user__nickname"),
            user_phone=F("user__phone"),
            user_user_type=F("user__user_type"),
            user_register_time=F("user__register_time"),
            verify_user_user_name=F("verify_user__user_name"),
            verify_user_nickname=F("verify_user__nickname"),
            verify_user_phone=F("verify_user__phone"),
            verify_user_user_type=F("verify_user__user_type"),
        ).extra(
            select={
                'verify_time': 'DATE_FORMAT(verify_time, "%%Y-%%m-%%d %%H:%%i:%%s")',
                'updated_time': 'DATE_FORMAT(updated_time, "%%Y-%%m-%%d %%H:%%i:%%s")',
                'created_time': 'DATE_FORMAT(created_time, "%%Y-%%m-%%d %%H:%%i:%%s")',
            }
        ).filter(**params).order_by(sort).values(
            "id", "apply_type_id", "user_id", "verify_user_id", "result", "remark",
            "reject_reason", "snapshot", "verify_files", "verify_time", "updated_time", "created_time",
            "apply_type_value", "apply_type_name",
            "user_user_name", "user_nickname", "user_phone", "user_user_type", "user_register_time",
            "verify_user_user_name", "verify_user_nickname", "verify_user_phone", "verify_user_user_type",
        )

        total = record_obj.count()
        paginator = Paginator(record_obj, size)

        try:
            page_set = paginator.page(page)
        except EmptyPage:
            return {'size': int(size), 'page': int(page), 'total': total, 'list': []}, None
        page_list = list(page_set.object_list)

        # 联动用户详细信息
        user_detail_list, err = DetailInfoService.get_list_detail(user_id_list=[i["user_id"] for i in page_list],
                                                                  filter_fields=["user_id", "real_name", "id_card"])
        verify_user_detail_list, err = DetailInfoService.get_list_detail(
            user_id_list=[i["verify_user_id"] for i in page_list], filter_fields=["user_id", "real_name"])
        user_detail_map = {i["user_id"]: i for i in user_detail_list}
        verify_user_detail_map = {i["user_id"]: i for i in verify_user_detail_list}
        for i in page_list:
            i.update(user_detail_map.get(i["user_id"], {}))
            # 替换key，添加前缀verify_
            current_user_verify_user_detail_map = verify_user_detail_map.get(i["verify_user_id"], {})
            if current_user_verify_user_detail_map:
                current_user_verify_user_detail_map = {"verify_" + k: v for k, v in
                                                       current_user_verify_user_detail_map.items()}
            i.update(current_user_verify_user_detail_map)

        return {'size': int(size), 'page': int(page), 'total': total, "result_to_cn": UserApplyServices.result_to_cn,
                'list': page_list}, None

    @staticmethod
    def apply_type_list(params: dict = None, **kwargs):
        return list(UserApplyType.objects.values()), None

    @staticmethod
    def apply_record_agg(params: dict = None, **kwargs):
        # 聚合查询统计计数
        result = UserApplyRecord.objects.values('apply_type_id', 'result').annotate(count=Count('id'))
        new_data = defaultdict(dict)
        [new_data[item['apply_type_id']].update({item['result']: item['count']}) for item in list(result)]
        return {'agg': new_data}, None
